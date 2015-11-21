import matcher_greedy as mg
from objects import *

# Simple asserting functions
def assertEquals(x,y):
	if x != y:
		raise Exception("[FAILURE] " + str(x) + " != " + str(y))
	else:
		print "Assertion passed!"

def assertNotEquals(x,y):
	if x == y or x is y:
		raise Exception("[FAILURE] " + str(x) + " != " + str(y))
	else:
		print "Assertion passed!"

# Give the matcher an easy optimal solution, and check that it finds it
def test_easy():
	students = [Student(x, [(0,9), (1,0)]) for x in range(3)]
	sections = [Section(0, 3), Section(1,3)]

	mg.match(students, sections)

	for s in students:
		assertEquals(s.assignment, 0)
	for i in range(2):
		assertEquals(sections[i].size, i*3)

# Give the matcher a large number of people who "don't care"
def test_dont_cares():
	students = []
	for i in range(1,4):
		students.append(Student(i, [(0,9), (1,0)]))
	for i in range(4,10):
		students.append(Student(i, [(0,2), (1,1)]))
	sections = [Section(x) for x in range(2)] 

	mg.match(students, sections)
	for s in students:
		if s.id < 4:
			assertEquals(s.assignment, 0)
	for s in students:
		assertNotEquals(s.assignment, None)	

# Give the matcher more people who want a section than it can hold
def test_unhappy():
	students = [Student(x, [(0,9), (1, 0)]) for x in range(1,10)]
	sections = [Section(0,3), Section(1,10)]

	mg.match(students, sections)

	assertEquals(len([x for x in students if x.assignment == 0]), 3)
	assertEquals(len([x for x in students if x.assignment == 1]), 6)

# Give the matcher more students than section capacity
def test_too_many_students():
	students = [Student(x, [(0,1)]) for x in range(10)]
	sections = [Section(0,3)]

	try:
		mg.match(students, sections)
		raise Exception("MatchImpossibleException should've been thrown, but wasn't.")
	except MatchImpossibleException:
		pass

# Run tests
for test in [test_easy, test_dont_cares, test_unhappy, test_too_many_students]:
	test()
