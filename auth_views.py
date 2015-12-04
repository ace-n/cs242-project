"""
Views responsible for authentication-related tasks (login/logout/passwords/authcodes)
"""
from lib.email_lib import Mail
from lib.security_lib import hash_password, secure_token
from lib.requirement_hooks import *
from lib.misc import json_status
from models import AuthcodeUser, PasswordUser 
from flask import Blueprint, redirect, session, render_template, request
from local_settings import ROOT_DOMAIN

auth_views = Blueprint('auth_views', __name__, template_folder='templates')

# Forgot password/authcode page
@auth_views.route('/auth/reset', methods=['GET', 'POST'])
def forgot_authentication():

	# Handle POST
	error_message = None
	if request.method == 'POST':

		# Get email
		email = request.form.get('email', '')
		if '@illinois.edu' not in email:
			if email == '' or '@' in email:
				error_message = 'Invalid email address. (Did you forget the @illinois.edu?)'
			else:
				# Accept netIDs too
				email = email + "@illinois.edu"

		# Do password/authcode reset
		if error_message is None:

			pw_query = PasswordUser.select().where(PasswordUser.email == email)
			authcode_query = AuthcodeUser.select().where(AuthcodeUser.email == email)

			if pw_query.exists() or authcode_query.exists():

				# Initialize mail object
				mail = Mail()
				mail.subject = "[CS242 Discussion Sections]"

				# Generate secure token
				token = secure_token()

				# Get user/email type
				if pw_query.exists():
					mail.subject += 'Password Reset'
					mail.message = 'Click the link below to reset your password.\n\n' + ROOT_DOMAIN + '/auth/reset/confirm?token=' + token

				else:
					mail.subject += 'Authcode Link'
					mail.message = 'Click the link below to authenticate.\n\n' + ROOT_DOMAIN + '/auth/code?token=' + token + '\n\nIf you have questions, please contact a TA.\n\nThanks,\nCS242 staff.'

				# Send mail
				mail.send([email])

				# If mail sent successfully, update user models
				if pw_query.exists():
					user = pw_query.get()
					user.password_reset_token = token
				else:
					user = authcode_query.get()
					user.authcode = token
				user.save()

				# Redirect to success page
				return render_template('reset-thanks.html')

			else:
				error_message = 'Your email isn\'t on our list. Ask a TA to add you to the site.'

	# Default/GET case
	return render_template('reset-form.html', error_message=error_message)

# Reset password page
# (Only for password-authenticated users)
@auth_views.route('/auth/reset/confirm', methods=['GET','POST'])
def reset_password():

	error_message = None

	# Handle GET (user clicked on email link)
	if request.method == 'GET':

		# Get token
		token = request.args.get('token', '')
		pw_query = PasswordUser.select().where(PasswordUser.password_reset_token == token)

		# Check for user
		if not pw_query.exists():
			return json_status(410, "Invalid token.")

		# Require long-enough reset token
		if len(token) != DEFAULT_TOKEN_LENGTH:
			return json_status(410, "Invalid token.")

		# Get user + construct password reset page
		user = pw_query.get()
		session['csrf_token'] = secure_token()  # To prevent CSRF
		session['reset_id'] = user.id

		# Invalidate user's existing password reset token
		user.password_reset_token = secure_token()
		user.save()

		# Show finished page
		return render_template('reset-newpassword.html', session=session)

	# Handle POST (user requested new password)
	else:
		requireCSRFToken()

		# Get user	
		user_query = PasswordUser.select().where(PasswordUser.id == session['reset_id'])
		if not user_query.exists():
			return json_status(500, "No matching user.")
		user = user_query.get()

		# Validate requested password
		password = request.form.get('password', '')
		if len(password) < 12 or len(set(password)) < 8:
			return render_template('reset-newpassword.html', session=session, error_message='Passwords must be 12+ characters long and contain 8+ different characters.')
		
		# Update user's password
		new_salt = secure_token()
		user.salt = new_salt
		user.salted_hash = hash_password(password, new_salt)
		user.save()

		# Redirect user to complete page
		return render_template('reset-complete.html')

# Login-via-password page
@auth_views.route('/auth/password', methods=['GET', 'POST'])
def login_password():

	# Handle POST
	error_message = None
	if request.method == 'POST':
		user_name = request.form.get('username', '')
		if '@illinois.edu' not in user_name:
			user_name += '@illinois.edu'
		pw = request.form.get('password', '')
		
		# Get user object
		user_query = PasswordUser.select().where(PasswordUser.email == user_name)

		# Check password
		if user_query.exists():
			user_obj = user_query.get()
			pw_encrypted = hash_password(pw, user_obj.salt)
			if pw_encrypted == user_obj.salted_hash:
				session['user_id'] = user_obj.id
				session['is_passworded'] = True
				session['csrf_token'] = secure_token(64)
				return redirect('/')
		
		# POST failed
		error_message = 'Invalid username and/or password.'
	
	# Handle GET/failed POST
	return render_template('login.html', error_message=error_message)

# Login via authcode page
@auth_views.route('/auth/code', methods=['GET'])
def login_authcode():

	# Get authcode
	authcode = request.args.get('token', None)
	if not authcode:
		return redirect('/auth/reset')
	
	# Get associated user
	user_query = AuthcodeUser.select().where(AuthcodeUser.authcode == authcode)
	if not user_query.exists():
		return redirect('/auth/reset')
	user_obj = user_query.get()

	# Log them in
	session['user_id'] = user_obj.id
	session['is_passworded'] = False
	session['csrf_token'] = secure_token()

	# Go to homepage
	return redirect('/')

# Logout
@auth_views.route('/auth/logout')
def logout():
	session['user_id'] = None
	session['is_passworded'] = False
	session['csrf_token'] = ''
	return render_template('logout.html')
