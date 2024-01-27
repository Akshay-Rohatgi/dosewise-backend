import tools, requests
import db
from flask import Flask, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Dosewise Backend'

@app.route('/api/v1/lookup')
def lookup():
    name = request.args.get('name').lower()
    return tools.get_data(f'https://api.fda.gov/drug/ndc.json?search=generic_name:"{name}"&limit=1')

# authentication, username and hashed password
@app.route('/api/v1/auth')
def auth():
    username = request.args.get('username')
    hash = request.args.get('hash')
    if db.get_hash(username) == hash:
        return 'true'
    else:
        return 'false'

if __name__ == '__main__':
    app.run(debug=True, port=8080)
