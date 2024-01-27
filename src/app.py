import tools, requests
from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def index():
    return 'Dosewise Backend'

# API to lookup medicine, for example /api/v1/lookup?name=Oseltamivir
@app.route('/api/v1/lookup')
def lookup():
    name = request.args.get('name').lower()
    return tools.get_data(f'https://api.fda.gov/drug/ndc.json?search=generic_name:"{name}"&limit=1')

    

if __name__ == '__main__':
    app.run(debug=True, port=8080)
