"""
A matching library that uses a Greedy algorithm
Takes O(students + sections) time
"""

import objects
from objects import MatchImpossibleException

"""
Calculate a greedily-maximal matching
@param students A list of Student objects
@param sections A list of Section objects
"""
def match(students, sections):

	assignments = []
	for rating in reversed(range(10)):
		
		# Get Students and Sections who gave a rating of $rating
		ratedStudents = []
		for student in [x for x in students if x.assignment == -1]:
			preferredSections = [x[0] for x in student.preferences if x[1] == rating]
			if len(preferredSections) != 0:
				ratedStudents.append((student, preferredSections))

		# Sort ratedStudents in ascending order by the number of sections each student picked
		ratedStudents = sorted(ratedStudents, key=lambda x: len(x[1]))
	
		# Assign each student to a section, where possible
		for rating in ratedStudents:
			for s in rating[1]:
				section = sections[s]
				if section.size > 0:
					section.size -= 1
					rating[0].assignment = section.id

	# Report failure to match (if any)
	for student in students:
		if student.assignment == -1:
			raise MatchImpossibleException("One or more students could not be matched.")	
