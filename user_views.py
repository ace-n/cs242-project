"""
Views responsible for user-related tasks (adding/deleting users)
NOTE: auth_views deals with auth-related tasks executed by a user themself,
      while user_views deals with any user task executed by another user
"""
import calendar
from lib.requirement_hooks import *
from lib.security_lib import hash_password, secure_token
from lib.misc import json_status
from models import *
from flask import Blueprint, redirect, session, render_template, request
from local_settings import ROOT_DOMAIN
from collections import OrderedDict
from event_hooks import *

user_views = Blueprint('user_views', __name__, template_folder='templates')

# [ADMIN] Manage users
@user_views.route('/users/manage')
def manage_users():
	requirePasswordedUser()
	requireCSRFToken()

	# Format section data
	sections = Section.select().order_by(Section.weekday, Section.time)
	section_days = OrderedDict((x, []) for x in calendar.day_name)
	for s in sections:
		section_days[s.weekday].append(s)

	# Done!
	return render_template('manage-users.html', session=session, password_users=PasswordUser.select(), authcode_users=AuthcodeUser.select())

# [ADMIN] Add a user via AJAX
@user_views.route('/users/add', methods=['POST'])
def add_user():
	requirePasswordedUser()
	requireCSRFToken()

	# Get data
	email = request.values.get('email', None)
	is_passworded = request.values.get('is_passworded', None)

	# Validate data
	if email is None or is_passworded is None: 
		return json_status(400, "One or more of (email, is_passworded) is missing.")
	if len(email) < 2 or len(email) > 256:
		return json_status(400, "Email must be between 2 and 256 (inclusive) characters long.")
	if '@' not in email:
		email += '@illinois.edu'
	elif '@illinois.edu' not in email:
		return json_status(400, "Emails must be either netids or @illinois.edu emails")
	is_passworded = is_passworded.lower()
	if is_passworded not in ["true", "false"]:
		return json_status(400, "Invalid is_passworded value")
	is_passworded = (is_passworded == "true")

	# Prevent duplication
	if PasswordUser.select().where(PasswordUser.email==email).exists() or AuthcodeUser.select().where(AuthcodeUser.email==email).exists():
		return json_status(400, "User already exists")

	# Create user
	password = None
	user = None
	if is_passworded:
		password = secure_token(12)
		salt = secure_token()
		salted_hash = hash_password(password, salt)
		user = PasswordUser(email=email, salt=salt, salted_hash=salted_hash)
	else:
		user = AuthcodeUser(email=email, authcode=secure_token())
	user.save()

	# Trigger event hooks (to notify the user)
	if is_passworded:
		on_create_password_user(user, password)
	else:
		on_create_authcode_user(user)

	# Done!
	return json_status(200, user.id)

# [ADMIN] Delete a user via AJAX
@user_views.route('/users/delete', methods=['POST'])
def delete_user():
	requirePasswordedUser()
	requireCSRFToken()
	
	# Get data
	email = request.values.get('email', None)
	if email is None:
		return json_status(400, "No email specified")
	if "@" not in email: 
		email += "@illinois.edu"
	elif "@illinois.edu" not in email:
		return json_status(400, "Invalid email")

	# Validate ID
	pw_query = PasswordUser.select().where(PasswordUser.email==email)
	ac_query = AuthcodeUser.select().where(AuthcodeUser.email==email)
	if not pw_query.exists() and not ac_query.exists():
		return json_status(410, "No matching user")

	# Do deletion
	if pw_query.exists():
		pw_query.get().delete_instance()
	else:
		ac_query.get().delete_instance()

	# Done!
	return json_status(200, None)
