"""
Requirement hooks throw errors unless certain (desired) conditions are True
"""
from flask import redirect, abort, session, request

# Require a valid CSRF token on a non-GET request
def requireCSRFToken():
	if request.method != 'GET':
		client_token = request.form.get('csrf_token', None)
		if not client_token:
			client_token = request.values.get('csrf_token', None)
		if not client_token or client_token != session.get('csrf_token', 'BAD'):
			abort(400)

# Require a passwordUser
def requirePasswordedUser():
	requireUser()
	if not session.get('is_passworded', False):
		abort(403)

# Require an authcodeUser
def requireAuthcodeUser():
	requireUser()
	if session.get('is_passworded', False):
		abort(403)

# Require any user
def requireUser():
	if session.get('user_id', None) is None:
		abort(401)
