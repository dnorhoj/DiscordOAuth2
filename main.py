from flask import Flask, render_template, request
from static import urls, auth
from urllib.parse import quote
import requests, api

app = Flask(__name__)
port = 8000

@app.route('/')
def index():
	redirect = quote(auth.redirect)
	scopes = quote(auth.scopes)

	url = urls.auth.format(urls.baseapi, auth.id, redirect, scopes)

	return render_template('index.html', url=url)

@app.route('/response')
def response():
	code = request.args.get('code')
	
	try:
		res = api.exchange_code(code)
	except requests.exceptions.HTTPError as e:
		return "Invalid Code, try again."

	try:
		user = api.get_info(res['access_token'])
	except requests.exceptions.HTTPError as e:
		print(e)
		return "Invalid Token, try again."

	return str(user)
	#return render_template('response.html')

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0',port=port)