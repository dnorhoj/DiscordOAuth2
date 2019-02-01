from flask import Flask, render_template, request, session, redirect, jsonify
from urllib.parse import quote
import requests, api, auth, time

app = Flask(__name__)
port = 8000
app.config['SECRET_KEY'] = auth.secretkey

# Endpoints
OAUTHURL = "https://discordapp.com/api/oauth2/authorize?client_id={}&redirect_uri={}&response_type=code&scope={}"

@app.route('/')
def index():
	redirect = quote(auth.redirect)
	scopes = quote(auth.scopes)

	url = OAUTHURL.format(auth.id, redirect, scopes)
	token = session.get('token')

	return render_template('index.html', url=url, token=token)

@app.route('/callback')
def response():
	code = request.args.get('code')
	
	try:
		res = api.exchange_code(code)
	except requests.exceptions.HTTPError:
		return "Invalid Code, try again."

	session['token'] = res['access_token']
	session['scopes'] = auth.scopes.split(" ")
	return redirect("/me")

@app.route('/newme')
def nme():
	if session.get('token') is None:
		return redirect("/")

	try:
		if "identify" in session.get('scopes'):
			user = api.get_info(session.get('token'))
		else:
			user = None

		if "guilds" in session.get('scopes'):
			guilds = jsonify(api.get_guilds(session.get('token')))
		else:
			guilds = None

		if "connections" in session.get('scopes'):
			connections = api.get_connections(session.get('token'))
		else:
			connections = None

	except requests.exceptions.HTTPError as e:
		return "Unexpected Error:<br>{}".format(e)
	
	print(guilds)

	if "email" in session.get('scopes'):
		email = True
	else:
		email = False

	print(session.get('scopes'))

	return render_template(
		'me.html',
		user=user,
		guilds=guilds,
		connections=connections,
		email=email
	)

@app.route('/me')
def me():
	if session.get('token') is None:
		return redirect("/")

	try:
		user = api.get_info(session.get('token'))
	except requests.exceptions.HTTPError:
		return "Invalid Token, try again."

	return jsonify(user)

@app.route('/guilds')
def guilds():
	if session.get('token') is None:
		return redirect('/')
	
	try:
		servers = api.get_guilds(session.get('token'))
	except requests.exceptions.HTTPError:
		return "Invalid Token, try again."
	
	return jsonify(servers)

@app.route('/connections')
def connections():
	if session.get('token') is None:
		return redirect('/')
	
	try:
		cons = api.get_connections(session.get('token'))
	except requests.exceptions.HTTPError:
		return "Invalid token or not enough permissions!"
	
	return jsonify(cons)

@app.route('/logout')
def logout():
	del session['token']
	
	return redirect('/')

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0',port=port)