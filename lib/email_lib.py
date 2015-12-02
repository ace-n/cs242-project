"""
Imports
"""

# Add root directory to path
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

# Do imports
import local_settings as constants
import smtplib


"""
Email sending functions
"""

# Mail object
class Mail:

	def __init__(self):
		self.author_name = "CS242 Discussion Section Scheduler"
		self.author = "mwoodley@illinois.edu"
		self.subject = ""
		self.message = ""

	# Send this email to a list of email addresses
	# @to_addrs A list of email addresses to send the mail to
	def send(self, to_addrs):

		# From http://www.nixtutor.com/linux/send-mail-through-gmail-with-python/
		server = smtplib.SMTP(constants.SMTP_SERVER)
		server.starttls()
		server.login(constants.GMAIL_USERNAME, constants.GMAIL_PASSWORD)
		server.sendmail(self.author, to_addrs, self.message)
		server.quit()
