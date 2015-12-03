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
			abort(500)

# Require a passwordUser
def requirePasswordedUser():
	if not session.get('is_passworded', False):
		redirect('/auth/password')

# Require any user
def requireUser():
	if not session.get('user_id', None):
		redirect('/auth/password')
