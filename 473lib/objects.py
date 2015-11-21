class MatchImpossibleException(Exception):
	pass

class Student(object):
	def __init__(self, id, preferences):
		self.id = id 
		self.preferences = preferences  # List of (section, rating) tuples
		self.assignment = -1

class Section(object):
	def __init__(self, id, size = 5):
		self.id = id
		self.size = size
