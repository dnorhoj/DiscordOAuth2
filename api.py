import auth
import requests

# Endpoints
BASEAPI = "https://discordapp.com/api"
ME_INFO = "/users/@me"
TOKEN = "/oauth2/token"
AUTH = "{}/oauth2/authorize?client_id={}&redirect_uri={}&response_type=code&scope={}"

def exchange_code(code):
	data = {
		'client_id': auth.id,
		'client_secret': auth.secret,
		'grant_type': 'authorization_code',
		'code': code,
		'redirect_uri': auth.redirect,
		'scope': auth.scopes
	}
	headers = {
		'Content-Type': 'application/x-www-form-urlencoded'
	}
	r = requests.post('{}{}'.format(BASEAPI, TOKEN), data, headers)
	r.raise_for_status()
	return r.json()

def get_info(token):
	headers = {
		'Authorization': 'Bearer {}'.format(token)
	}
	
	r = requests.get('{}{}'.format(BASEAPI, ME_INFO), headers=headers)
	r.raise_for_status()
	return r.json()