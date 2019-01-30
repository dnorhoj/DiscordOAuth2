from flask import Flask, render_template, request, session, redirect, jsonify
from urllib.parse import quote
import requests, api, auth

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
	return redirect("/me")

@app.route('/me')
def me():
	if session.get('token') is None:
		return redirect("/")

	try:
		user = api.get_info(session.get('token'))
	except requests.exceptions.HTTPError:
		return "Invalid Token, try again."

	return jsonify(user)
	#return render_template('response.html')

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