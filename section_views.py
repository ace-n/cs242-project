"""
Views responsible for section-related tasks (adding/editing/deleting/picking sections)
"""
import calendar
from lib.requirement_hooks import *
from models import Section 
from flask import Blueprint, redirect, abort, session, render_template, request
from local_settings import ROOT_DOMAIN

section_views = Blueprint('section_views', __name__, template_folder='templates')

# Pick sections
@section_views.route('/sections/pick')
def pick_sections():
	requireUser()
	requireCSRFToken()
	return render_template('pick-sections.html', session=session)

# [ADMIN] Manage sections
@section_views.route('/sections/manage')
def manage_sections():
	requirePasswordedUser()
	requireCSRFToken()

	# Format section data
	sections = Section.select()
	section_days = {x:[] for x in calendar.day_name}
	for s in sections:
		section_days[s.weekday].append(s)

	# Done!
	return render_template('manage-sections.html', session=session, section_days=section_days)

# [ADMIN] Add a section via AJAX
@section_views.route('/sections/add', methods=['POST'])
def add_section():
	requireCSRFToken()

	# Get data
	day = request.values.get('day', None)
	time = request.values.get('time', None)

	# Validate data
	if day is None or time is None:
		return 'ERROR: day and/or time is invalid.'
	day = day.title()
	if len(day) > 10 or len(time) > 10:
		return 'ERROR: day and time must be 10 characters or less'
	if day not in calendar.day_name:
		return 'ERROR: day must be one of [' + ','.join(calendar.day_name.title()) + '] (case insensitive)'

	# Create section
	s = Section(weekday=day, time=time)
	s.save()

	# Done!
	return 'success' 

# [ADMIN] Delete a section via AJAX
@section_views.route('/sections/delete', methods=['POST'])
def delete_section():
	requireCSRFToken()
	return 'Not yet implemented'

# [ADMIN] Edit a section via AJAX
@section_views.route('/sections/edit', methods=['POST'])
def edit_section():	
	requireCSRFToken()
	return 'Not yet implemented'
