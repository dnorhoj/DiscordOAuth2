from flask import Flask, render_template, request
import urls, requests

app = Flask(__name__)
port = 8000

@app.route('/')
def index():
	url = urls.auth.format("464532048833544193")
	return render_template('index.html', url=url)

@app.route('/response')
def response():
	code = request.args.get('code')
	res = requests.post(urls.converttoken.format(code))
	print(res.text)
	print(code)
	return res.text
	#return render_template('response.html')

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0',port=port)