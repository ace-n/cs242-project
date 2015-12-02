from models import AuthcodeUser, PasswordUser 
from flask import Blueprint, Flask, redirect, abort, session, render_template, request
from local_settings import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Include various views
from auth import auth_views
app.register_blueprint(auth_views)

# Detect a number
def __isdigit(x):
	try:
		int(x)
		return True
	except:
		return False

# Homepage
@app.route('/')
def home():
	return render_template('index.html', session=session)

# Pick sections
@app.route('/sections/pick')
def pick_sections():
	requireUser()
	requireCSRFToken(request)
	return render_template('pick-sections.html', session=session)

# [ADMIN] Manage sections
@app.route('/sections/manage')
def manage_sections():
	requirePasswordedUser()
	requireCSRFToken(request)
	return render_template('manage-sections.html', session=session)

# [ADMIN] Add a section via AJAX
@app.route('/sections/add', methods=['POST'])
def add_section():
	requireCSRFToken(request)
	return 'Not yet implemented'

# [ADMIN] Delete a section via AJAX
@app.route('/sections/delete', methods=['POST'])
def delete_section():
	requireCSRFToken(request)
	return 'Not yet implemented'

# [ADMIN] Edit a section via AJAX
@app.route('/sections/edit', methods=['POST'])
def edit_section():	
	requireCSRFToken(request)
	return 'Not yet implemented'


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
