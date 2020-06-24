import re
import hashlib
from flask import Blueprint, render_template, request, url_for, redirect, session

from database import db, User

login = Blueprint('login', __name__)
logout = Blueprint('logout', __name__)


def verify_email(email):
    email_pat = re.compile('^[A-Za-z0-9_\-.]+@[A-Za-z0-9_\-.]+\.[A-Za-z]{2,4}')
    return bool(re.match(email_pat, email))


def verify_login(sess):
    # Verify login information
    if 'username' not in sess or 'password' not in sess:
        return False
    user, pwd = sess['username'], sess['password']
    # Fetch true password from dataset
    hit_user = User.query.filter_by(username=user).first()
    # Either not exist or password error
    if not hit_user or pwd != hit_user.password:
        return False
    return True


@login.route('/', methods=('GET', 'POST'))
def login_func():
    error = None
    if request.method == 'POST':
        # Get data
        is_register = request.form['is_register'] == 'yes'
        user, pwd = request.form['name'], request.form['pwd']
        email = ''
        if is_register:
            email = request.form['email']

        # Check input format
        if not user or not pwd:
            error = '用户名/密码不能为空'
        if not 6 <= len(user) <= 20 or not 6 <= len(pwd) <= 20:
            error = '用户名/密码长度应该在6到20字之间'
        if is_register and not verify_email(email):
            error = '邮箱格式错误'

        # Crypt password
        pwd = hashlib.sha1(pwd.encode('utf-8')).hexdigest()

        # Login / register
        if not error:
            if is_register:
                # Register user: make sure the user name & email is unique
                hit_user = User.query.filter_by(username=user).first()
                hit_email = User.query.filter_by(email=email).first()
                if hit_user or hit_email:
                    error = '用户名/邮箱已被注册'
                else:
                    # Register user
                    user_entry = User(username=user, password=pwd, email=email)
                    db.session.add(user_entry)
                    db.session.commit()
            else:
                # Login user
                hit_user = User.query.filter_by(username=user).first()
                # Either not exist or password error
                if not hit_user or pwd != hit_user.password:
                    error = '用户登录失败'

        if error:
            return render_template('login.html', error=error)

        else:
            session['message'] = '用户{}成功！'.format(['登录', '注册'][is_register])
            session['message_type'] = 'info'
            session['username'] = user
            session['password'] = pwd
            return redirect(url_for('home.home_func'))

    elif verify_login(session):
        # Already logged in, redirect to home page
        return redirect(url_for('home.home_func'))

    else:
        # Register / login
        return render_template('login.html', error=error)


@logout.route('/')
def logout_func():
    name = session.pop('username', '?')
    session.pop('password', None)
    session['message'] = '用户已注销！再见，' + name
    session['message_type'] = 'info'
    return redirect(url_for('home.home_func'))
