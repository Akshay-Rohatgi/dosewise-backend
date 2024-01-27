import tools, requests
from flask import Flask, request, flask_cors
from flask_cors import cross_origin
app = Flask(__name__)

@app.route('/')
def index():
    return 'Dosewise Backend'

@app.route('/api/v1/lookup')
@cross_origin()
def lookup():
    name = request.args.get('name').lower()
    return tools.get_data(f'https://api.fda.gov/drug/ndc.json?search=generic_name:"{name}"&limit=1')

# authentication, username and hashed password
@app.route('/api/v1/auth')
def auth():
    username = request.args.get('username')
    hash = request.args.get('hash')
    if hash == '123456' and username == 'admin':
        return 'SUCCESS'
    else:
        return 'FAILURE'

if __name__ == '__main__':
    app.run(debug=True, port=8080)
