import hashlib
from models import AuthcodeUser, PasswordUser 
from flask import Flask, redirect, abort, session, render_template, request
from local_settings import secret_key

app = Flask(__name__)
app.secret_key = secret_key

# Require a passwordUser
def requirePasswordedUser():
	if not session.get('is_passworded', False):
		redirect('/auth/password')

# Require any user
def requireUser():
	if not session.get('user_id', None):
		redirect('/auth/password')

# Detect a number
def __isdigit(x):
	try:
		int(x)
		return True
	except:
		return False

# Reset password
@app.route('/auth/password/reset')
def reset_password():
	return render_template('reset-form.html')

# Reset authcode
@app.route('/auth/code/reset')
def reset_authcode():
	return render_template('reset-form.html')

# Login-via-password page
@app.route('/auth/password', methods=["GET", "POST"])
def login_password():

	# Handle POST
	error_message = None
	if request.method == "POST":
		user_name = request.form.get("username", "")
		if "@illinois.edu" not in user_name:
			user_name += "@illinois.edu"
		pw = request.form.get("password", "")
		
		# Get user object
		user_query = PasswordUser.select().where(PasswordUser.email == user_name)

		# Check password
		if user_query.exists():
			user_obj = user_query.get()
			pw_encrypted = hashlib.sha512(pw + user_obj.salt).hexdigest()
			if pw_encrypted == user_obj.salted_hash:
				session['user_id'] = user_obj.id
				session['is_passworded'] = True
				session['csrf_token'] = "TODO-change-me"
				return redirect('/')
		
		# POST failed
		error_message = "Invalid username and/or password."
	
	# Handle GET/failed POST
	return render_template('login.html', error_message=error_message)

# Login via authcode page
@app.route('/auth/code', methods=['GET'])
def login_authcode():

	# Get authcode
	authcode = request.args.get("code", None)
	if not authcode:
		return redirect("/auth/code/reset")
	
	# Get associated user
	user_query = AuthcodeUser.select().where(AuthcodeUser.authcode == authcode)
	if not user_query.exists():
		return redirect("/auth/code/reset")
	user_obj = user_query.get()

	# Log them in
	session['user_id'] = user_obj.id
	session['is_passworded'] = False
	session['csrf_token'] = "TODO-change-me"

	# Go to homepage
	return redirect('/')

# Logout
@app.route('/auth/logout')
def logout():
	session['user_id'] = None
	session['is_passworded'] = False
	session['csrf_token'] = ''
	return render_template("logout.html")

# Homepage
@app.route('/')
def home():
	return render_template('index.html', session=session)

# Pick sections
@app.route('/sections/pick')
def pick_sections():
	requireUser()
	return render_template('pick-sections.html', session=session)

# [ADMIN] Manage sections
@app.route('/sections/manage')
def manage_sections():
	requirePasswordedUser()
	return render_template('manage-sections.html')

# [ADMIN] Add a section via AJAX
@app.route('/sections/add', methods=["POST"])
def add_section():
	requireCSRFToken(request)
	return "Not yet implemented"

# [ADMIN] Delete a section via AJAX
@app.route('/sections/delete', methods=["POST"])
def delete_section():
	requireCSRFToken(request)
	return "Not yet implemented"

# [ADMIN] Edit a section via AJAX
@app.route('/sections/edit', methods=["POST"])
def edit_section():	
	requireCSRFToken(request)
	return "Not yet implemented"


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
