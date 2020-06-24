from app import app
from pages import home, login, logout, design, manage, fill, analyze

# Register page blueprints as routes
app.register_blueprint(home, url_prefix='/')
app.register_blueprint(login, url_prefix='/login')
app.register_blueprint(logout, url_prefix='/logout')
app.register_blueprint(design, url_prefix='/design')
app.register_blueprint(fill, url_prefix='/fill')
app.register_blueprint(manage, url_prefix='/manage')
app.register_blueprint(analyze, url_prefix='/analyze')

# Start app
app.run()
