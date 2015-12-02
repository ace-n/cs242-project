"""
Requirement hooks throw errors unless certain (desired) conditions are True
"""
from flask import redirect, abort, session, request

# Require a valid CSRF token on a non-GET request
def requireCSRFToken():
	if request.method != 'GET' and session.get('csrf_token', 'a') != request.form.get('csrf_token', 'b'):
		abort(500)

# Require a passwordUser
def requirePasswordedUser():
	if not session.get('is_passworded', False):
		redirect('/auth/password')

# Require any user
def requireUser():
	if not session.get('user_id', None):
		redirect('/auth/password')
