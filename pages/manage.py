import json
import datetime
from flask import Blueprint, request, url_for, redirect, session, current_app, render_template

from database import Survey, db, model2dict
from pages import verify_login

manage = Blueprint('manage', __name__)


@manage.route('/', methods=('GET', 'POST'))
def manage_func():
    # Login required
    if not verify_login(session):
        return redirect(url_for('login.login_func'))
    if request.method == 'POST':
        info = json.loads(str(request.data, encoding='utf-8'))
        action, survey_id = info['action'], info['survey_id']
        operation_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            survey_obj = Survey.query.filter_by(index=survey_id).first()
            if action == 'delete':
                # Delete the survey
                db.session.delete(survey_obj)
            if action == 'publish':
                # Publish the survey
                survey_obj.status = True
                survey_obj.publish_time = operation_time
            db.session.commit()
        except Exception as e:
            current_app.logger.error(
                'Failed to perform action: ' + info['action'] + 'because of ' + str(e))
            return json.dumps({'status': 'fail', 'time': operation_time})
        else:
            return json.dumps({'status': 'success', 'time': operation_time})

    else:
        # Get user's survey data
        user = session['username']
        survey_objs = Survey.query.filter_by(username=user).all()
        survey_dicts = [model2dict(survey_obj) for survey_obj in survey_objs]
        return render_template('manage.html',
                               username=user,
                               survey=json.dumps(survey_dicts))
