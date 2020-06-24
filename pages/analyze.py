import json
import datetime
from flask import Blueprint, render_template, url_for, redirect, session

from database import Survey, get_survey_data, get_submit_data
from pages import verify_login

analyze = Blueprint('analyze', __name__)


@analyze.route('/<survey_id>', methods=('GET',))
def analyze_func(survey_id):
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

    # Get survey data
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    survey_dict, question_dicts, all_option_dicts = get_survey_data(survey_id)
    submit_dicts, all_answer_dicts = get_submit_data(survey_id)

    return render_template('analyze.html',
                           username=user,
                           time=current_time,
                           survey=json.dumps(survey_dict),
                           questions=json.dumps(question_dicts),
                           options=json.dumps(all_option_dicts),
                           submits=json.dumps(submit_dicts),
                           answers=json.dumps(all_answer_dicts))
