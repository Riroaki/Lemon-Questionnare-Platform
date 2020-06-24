from flask import Blueprint, render_template, session

from pages import verify_login

home = Blueprint('home', __name__)


# Home page
@home.route('/')
def home_func():
    user, msg, msg_type = None, None, None
    if 'message' in session:
        msg, msg_type = session['message'], session['message_type']
    if verify_login(session):
        user = session['username']
    return render_template('index.html',
                           username=user,
                           message=msg,
                           message_type=msg_type)
