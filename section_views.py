"""
Views responsible for section-related tasks (adding/editing/deleting/picking sections)
"""
import calendar
from lib.requirement_hooks import *
from lib.misc import json_status
from models import Section 
from flask import Blueprint, redirect, session, render_template, request
from local_settings import ROOT_DOMAIN
from collections import OrderedDict

section_views = Blueprint('section_views', __name__, template_folder='templates')

# Pick sections
@section_views.route('/sections/pick')
def pick_sections():
	requireUser()
	requireCSRFToken()

	# Format section data
	sections = Section.select().order_by(Section.weekday, Section.time)
	section_days = OrderedDict((x, []) for x in calendar.day_name)
	for s in sections:
		section_days[s.weekday].append(s)

	return render_template('pick-sections.html', session=session, section_days=section_days)

# [ADMIN] Manage sections
@section_views.route('/sections/manage')
def manage_sections():
	requirePasswordedUser()
	requireCSRFToken()

	# Format section data
	sections = Section.select().order_by(Section.weekday, Section.time)
	section_days = OrderedDict((x, []) for x in calendar.day_name)
	for s in sections:
		section_days[s.weekday].append(s)

	# Done!
	return render_template('manage-sections.html', session=session, section_days=section_days)

# [ADMIN] Add/Update a section via AJAX
@section_views.route('/sections/change', methods=['POST'])
def change_section():
	requirePasswordedUser()
	requireCSRFToken()

	# Get data
	weekday = request.values.get('weekday', None)
	time = request.values.get('time', None)
	id = request.values.get('id', None)
	if id == '':
		id = None

	# Validate data
	if weekday is None or time is None:
		return json_status(400, "Missing weekday and/or time field.")
	weekday = weekday.title()
	if weekday not in calendar.day_name:
		return json_status(400, "Invalid weekday name.")

	# Create/fetch section
	if id is None:
		section = Section(weekday=weekday, time=time)
	else:
		query = Section.select().where(Section.id==id)
		if not query.exists():
			json_status(410, "Invalid section id.")
		section = query.get()
		section.weekday = weekday
		section.time = time

	# Update section
	section.save()

	# Done!
	return json_status(200, section.id) 

# [ADMIN] Delete a section via AJAX
@section_views.route('/sections/delete', methods=['POST'])
def delete_section():
	requirePasswordedUser()
	requireCSRFToken()
	
	# Get data
	id = request.values.get('id', None)
	if id is None:
		return json_status(400, "Missing section id.")

	# Validate ID
	query = Section.select().where(Section.id==id)
	if not query.exists():
		return json_status(410, "Invalid section id.")

	# Do deletion
	query.get().delete_instance()

	# Done!
	return json_status(200, None)
