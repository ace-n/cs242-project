from peewee import *
#from peewee import create_model_tables
#create_model_tables([PasswordUser])

class BaseModel(Model):
	class Meta:
		database = MySQLDatabase("cs242_discussions", user="root", password="")

class Section(BaseModel):
	weekday = CharField(max_length=10)
	time = CharField(max_length=10)

# Abstract model, should never be instantiated
class User(BaseModel):
	email = CharField(max_length=256)
	section = ForeignKeyField(Section, null=True, default=None)

class PasswordUser(User):
	salted_hash = CharField(max_length=256)
	salt = CharField(max_length=256)
	password_reset_token = CharField(max_length=256)

class AuthcodeUser(User):
	authcode = CharField(max_length=256)
