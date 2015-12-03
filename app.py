from models import AuthcodeUser, PasswordUser 
from flask import Blueprint, Flask, redirect, abort, session, render_template, request
from local_settings import SECRET_KEY
from lib.requirement_hooks import *

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Include various views
from auth_views import auth_views
from section_views import section_views
app.register_blueprint(auth_views)
app.register_blueprint(section_views)

# Homepage
@app.route('/')
def home():
	return render_template('index.html', session=session)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
