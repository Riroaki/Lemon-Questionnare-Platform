import json
import datetime
from flask import Blueprint, render_template, request, url_for, redirect, session, \
    current_app

from database import db, Survey, Question, Option, get_survey_data
from pages import verify_login

design = Blueprint('design', __name__)


def parse_save_survey_data(info_dict, new_survey=False):
    # Parse and create survey object / question objects / option objects
    # Survey object
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    survey_obj = Survey(title=info_dict['title'],
                        username=info_dict['username'],
                        desc=info_dict['desc'],
                        status=info_dict['status'],
                        answer_type=info_dict['answer_type'],
                        update_time=current_time,
                        publish_time=info_dict['publish_time'])

    # Use old index if any
    if not new_survey:
        survey_obj.index = info_dict['index']

    # If modifying a new survey, needs to republish it
    if survey_obj.status:
        survey_obj.publish_time = current_time

    # Add and flush session to get the index of survey
    db.session.add(survey_obj)
    db.session.flush()
    survey_index = survey_obj.index

    # Question objects
    question_objs = []

    for question in info_dict['questions']:
        question_obj = Question(title=question['title'],
                                type=question['type'],
                                survey_id=survey_index,
                                question_index=question['question_index'],
                                num_choices=question['num_choices'],
                                num_min_chosen=question['num_min_chosen'],
                                num_max_chosen=question['num_max_chosen'],
                                single_row=question['single_row'],
                                fill_digit=question['fill_digit'],
                                levels=question['levels'],
                                compulsory=question['compulsory'])
        question_objs.append(question_obj)

    # Add and flush session to get the indices of questions
    for question_obj in question_objs:
        db.session.add(question_obj)
    db.session.flush()
    question_indices = [question_obj.index for question_obj in question_objs]

    # Option objects
    for options, question_index in zip(info_dict['options'], question_indices):
        for option in options:
            option_obj = Option(question_id=question_index,
                                option_index=option['option_index'],
                                text=option['text'])
            db.session.add(option_obj)

    db.session.commit()

    return survey_index


@design.route('/', methods=('GET', 'POST'))
def design_func_new():
    # Design a new survey
    # Login required
    if not verify_login(session):
        return redirect(url_for('login.login_func'))
    user = session['username']

    if request.method == 'POST':
        # Parse and save the survey data
        try:
            info = json.loads(str(request.data, encoding='utf-8'))
            survey_id = parse_save_survey_data(info, new_survey=True)
        except Exception as e:
            current_app.logger.error('Failed to save data because of: ' + str(e))
            return json.dumps({'status': 'fail', 'survey_id': -1})
        else:
            return json.dumps({'status': 'success', 'survey_id': survey_id})

    else:
        # Create a new survey
        return render_template('design.html',
                               username=user,
                               survey='null',
                               questions='null',
                               options='null')


@design.route('/<survey_id>', methods=('GET', 'POST'))
def design_func_old(survey_id):
    # Modify a survey that is already present in database
    # Login required
    if not verify_login(session):
        return redirect(url_for('login.login_func'))
    user = session['username']

    # Check whether survey index is legal and priviledges
    error = None
    survey_obj = Survey.query.filter_by(index=survey_id).first()
    if not survey_obj:
        error = '啊哦，问卷好像走丢了'
    elif survey_obj.username != user:
        error = '抱歉，你没有权限编辑此问卷'
    if error:
        session['message'] = error
        session['message_type'] = 'error'
        return redirect(url_for('home.home_func'))

    if request.method == 'POST':
        # Save modifications for an old survey: delete old survey first
        # Will cascade delete all submissions related and all old questions
        survey_obj = Survey.query.filter_by(index=survey_id).first()
        if survey_obj:
            db.session.delete(survey_obj)
            db.session.commit()
        # Parse and save the survey data
        try:
            info = json.loads(str(request.data, encoding='utf-8'))
            survey_id = parse_save_survey_data(info)
        except Exception as e:
            current_app.logger.error('Failed to save data because of: ' + str(e))
            return json.dumps({'status': 'fail', 'survey_id': -1})
        else:
            return json.dumps({'status': 'success', 'survey_id': survey_id})

    else:
        survey_dict, question_dicts, all_option_dicts = get_survey_data(survey_id)
        return render_template('design.html',
                               username=user,
                               survey=json.dumps(survey_dict),
                               questions=json.dumps(question_dicts),
                               options=json.dumps(all_option_dicts))
