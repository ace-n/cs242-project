from peewee import *
#from peewee import create_model_tables
#create_model_tables([UserSectionRating])

# DB preferences
class BaseModel(Model):
	class Meta:
		database = MySQLDatabase("cs242_discussions", user="root", password="")

# A discussion section on a specific weekday and time
class Section(BaseModel):
	weekday = CharField(max_length=10)
	time = CharField(max_length=10)

# A base user model
# @note Abstract model, should never be instantiated
class User(BaseModel):
	email = CharField(max_length=256)
	section = ForeignKeyField(Section, null=True, default=None)

# A user who signs in via email/password (i.e. a professor/TA)
class PasswordUser(User):
	salted_hash = CharField(max_length=256)
	salt = CharField(max_length=256)
	password_reset_token = CharField(max_length=256)

# A user who signs in via an emailed authcode (i.e. a student)
class AuthcodeUser(User):
	authcode = CharField(max_length=256)

# Store a (user, section, rating) tuple
# Many-to-many relationship between AuthcodeUsers and Sections
class UserSectionRating(BaseModel):
	user = ForeignKeyField(AuthcodeUser, related_name="section_ratings")
	section = ForeignKeyField(Section, related_name="ratings")
	rating = IntegerField()
