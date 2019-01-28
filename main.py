from flask import Flask, render_template, request, session, redirect, jsonify
from static import urls, auth
from urllib.parse import quote
import requests, api

app = Flask(__name__)
port = 8000
app.config['SECRET_KEY'] = auth.secretkey

@app.route('/')
def index():
	redirect = quote(auth.redirect)
	scopes = quote(auth.scopes)

	url = urls.auth.format(urls.baseapi, auth.id, redirect, scopes)

	return render_template('index.html', url=url)

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
	print(session['token'])

	try:
		user = api.get_info(session['token'])
	except requests.exceptions.HTTPError:
		return "Invalid Token, try again."

	return jsonify(user)
	#return render_template('response.html')

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0',port=port)