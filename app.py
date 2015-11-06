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

# Reset authcode page
@app.route('/auth/reset_password')
def reset_password():
	return render_template('reset-form.html')

# Reset password page
@app.route('/auth/reset_password')
def reset_authcode():
	return render_template('reset-form.html')

# Homepage
@app.route('/')
def home():	
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
