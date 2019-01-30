import auth
import requests

# Endpoint
BASEAPI = "https://discordapp.com/api"

def _getheaders(token):
	return {
		'Authorization': 'Bearer {}'.format(token)
	}

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
	r = requests.post('{}/oauth2/token'.format(BASEAPI), data, headers)
	r.raise_for_status()
	return r.json()

def get_info(token):
	headers = _getheaders(token)

	r = requests.get('{}/users/@me'.format(BASEAPI), headers=headers)
	r.raise_for_status()
	return r.json()

def get_guilds(token):
	headers = _getheaders(token)

	r = requests.get('{}/users/@me/guilds'.format(BASEAPI), headers=headers)
	r.raise_for_status()
	return r.json()

def get_connections(token):
	headers = _getheaders(token)

	r = requests.get('{}/users/@me/connections'.format(BASEAPI), headers=headers)
	r.raise_for_status()
	return r.json()