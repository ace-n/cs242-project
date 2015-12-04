import Crypto.Random.random as rand
import hashlib
import string

# Given a password and salt, compute their hash
def hash_password(password, salt):
	cur = password + salt

	# Repeatedly hash the password, to make brute forcing more expensive
	for _ in range(10000):
		cur = hashlib.sha512(cur).hexdigest()

	# Done!
	return cur

# Securely generate a token (random, unique string)
# @param length The length of the token characters
DEFAULT_TOKEN_LENGTH = 256
def secure_token(length = DEFAULT_TOKEN_LENGTH):
	return "".join([rand.choice(string.hexdigits) for _ in range(length)])
