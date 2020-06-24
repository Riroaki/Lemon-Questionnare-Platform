from datetime import timedelta
from flask import session, Flask

from config import SECRET_KEY

# Initialize app
app = Flask(__name__)
app.secret_key = SECRET_KEY


# Set session expiration: 30 mins
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)
