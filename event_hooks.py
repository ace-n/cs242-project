"""
Event hooks that can be (easily) modified to change the behavior of the website
"""
from local_settings import ROOT_DOMAIN
from lib.email_lib import Mail

# Called whenever a password user is created
# @param user A recently created PasswordUser
def on_create_password_user(user, password):
	m = Mail()
	m.subject += "Your account details"
	m.message  = "Hello,\n\nAn account has been created for you." 
	m.message += "Your temporary password is (without quotes) '" + password + "'.\n\n"
	m.message += "To log in, click the link below and enter your temporary password.\n\n" + ROOT_DOMAIN + "/auth/password"
	m.send([user.email])

# Called whenever an authcode user is created
# @param user A recently created AuthcodeUser
def on_create_authcode_user(user):
	m = Mail()
	m.subject += "Your account details"
	m.message  = "Hello,\n\nAn account has been created for you."
	m.message += "To log in, click the link below.\n\n" + ROOT_DOMAIN + "/auth/code?token=" + user.authcode
	m.message += "\n\nOnce you've logged in, go to " + ROOT_DOMAIN + "/sections/pick to pick your preferred sections."
	m.send([user.email])
