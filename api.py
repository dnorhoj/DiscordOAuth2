from static import urls, auth
import requests

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
	r = requests.post('{}/oauth2/token'.format(urls.baseapi), data, headers)
	r.raise_for_status()
	return r.json()

def get_info(token):
	headers = {
		'Authorization': 'Bearer {}'.format(token)
	}
	
	r = requests.get('{}/users/@me'.format(urls.baseapi), headers=headers)
	r.raise_for_status()
	return r.json()