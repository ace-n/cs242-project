from peewee import *

class BaseModel(Model):
	class Meta:
		database = MySQLDatabase("cs242-discussions", user="root", password="")

class User(BaseModel):
	email = CharField(max_length=256)

class PasswordUser(User):
	salted_hash = CharField(max_length=256)
	salt = CharField(max_length=256)

class AuthcodeUser(User):
	authcode = CharField(max_length=256)
