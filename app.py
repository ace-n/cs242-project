from models import AuthcodeUser, PasswordUser 
from flask import Flask, abort, render_template, request
app = Flask(__name__)

# Detect a number
def __isdigit(x):
	try:
		int(x)
		return True
	except:
		return False

# Reset password
@app.route('/auth/reset_password')
def reset_password():
	return render_template('reset-form.html')

# Reset authcode
@app.route('/auth/reset_authcode')
def reset_authcode():
	return render_template('reset-form.html')

# Login page
@app.route('/auth/login')
def login():
	return render_template('login.html')

# Homepage
@app.route('/')
def home():	
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
