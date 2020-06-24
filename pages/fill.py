import json
import datetime
from flask import Blueprint, render_template, request, url_for, redirect, session, current_app

from database import db, Survey, Question, Submit, Answer, get_survey_data, model2dict
from pages import verify_login

fill = Blueprint('fill', __name__)


def parse_submit_answer(info_dict):
    # Parse and create submit object / answer objects
    submit_obj = Submit(survey_id=info_dict['survey_id'],
                        submit_ip=info_dict['submit_ip'],
                        username=info_dict['username'],
                        submit_date=info_dict['submit_date'])
    db.session.add(submit_obj)
    db.session.flush()
    submit_id = submit_obj.index

    # Create answer objects
    for answer, question in zip(info_dict['answers'], info_dict['questions']):
        answer_obj = Answer(question_id=question['index'],
                            submit_id=submit_id,
                            survey_id=info_dict['survey_id'],
                            type=question['type'],
                            content=json.dumps(answer))
        db.session.add(answer_obj)
    db.session.commit()


@fill.route('/<survey_id>', methods=('GET', 'POST'))
def fill_func(survey_id):
    # Check availability: whether the survey exist, and whether it's published
    survey_obj = Survey.query.filter_by(index=survey_id).first()
    survey_available = survey_obj and survey_obj.status
    error_prompts = ['啊哦，问卷好像走丢了', '请登录后再填写本问卷',
                     '已经超出填写次数限制', '已经超出今日填写次数限制，请改日再来']
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    user = ''
    if verify_login(session):
        user = session['username']

    # Fill survey
    error = -1
    if not survey_available:
        error = 0
    # Check whether requires login but this user didn't
    elif survey_obj.answer_type == 0 and not verify_login(session):
        error = 1
    # Check whether filling time exceeds
    elif survey_obj.answer_type < 0:
        # Allow one user to answer for a few times
        max_filling = abs(survey_obj.answer_type)
        fill_times = Submit.query.filter_by(submit_ip=request.remote_addr).count()
        if fill_times >= max_filling:
            error = 2
    elif survey_obj.answer_type > 0:
        # Allow one user to answer for a few times in a day
        max_filling = abs(survey_obj.answer_type)
        fill_times = Submit.query.filter(Submit.submit_ip == request.remote_addr,
                                         Submit.submit_date == today).count()
        if fill_times >= max_filling:
            error = 3

    if request.method == 'GET':
        # If an error occurs, just redirect
        if error != -1:
            session['message'] = error_prompts[error]
            session['message_type'] = 'error'
            return redirect(url_for('home.home_func'))

        survey_dict, question_dicts, all_option_dicts = get_survey_data(survey_id)
        return render_template('fill.html',
                               username=user,
                               survey=json.dumps(survey_dict),
                               questions=json.dumps(question_dicts),
                               options=json.dumps(all_option_dicts))

    else:
        # Request with error will not be allowed
        if error != -1:
            return json.dumps({'status': 'fail',
                               'reason': error_prompts[error]})

        try:
            # Collect all survey data: questions, options
            question_objs = Question.query.filter_by(survey_id=survey_id).all()
            # Sort questions
            question_objs = sorted(question_objs, key=lambda q: q.question_index)
            # Convert model to dict
            question_dicts = [model2dict(question_obj) for question_obj in question_objs]

            # Dump submission data
            info = json.loads(str(request.data, encoding='utf-8'))
            info['submit_ip'] = request.remote_addr
            info['username'] = user
            info['submit_date'] = today
            info['questions'] = question_dicts

            # Submit answer
            parse_submit_answer(info)
        except Exception as e:
            current_app.logger.error('Failed to submit answer because of: ' + str(e))
            return json.dumps({'status': 'fail',
                               'reason': error_prompts[error]})
        else:
            return json.dumps({'status': 'success'})
