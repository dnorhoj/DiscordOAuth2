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
	
	res = api.exchange_code(code)
	print(res)
	return str(res)
	#return render_template('response.html')

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0',port=port)