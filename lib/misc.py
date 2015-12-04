import json

def json_status(status_code, message):
	d = {"status": status_code}
	if message is not None:
		d["message"] = message
	return json.dumps(d)
