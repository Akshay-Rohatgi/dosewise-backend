import tools, requests
import db, lookups
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
    return lookups.lookup_medicine_fda(name)

@app.route('/api/v1/add')
def add():
    username = request.args.get('username')
    hash = request.args.get('hash')
    if db.get_hash(username) == hash:
        name = request.args.get('name')
        manufacturer_name = request.args.get('manufacturer_name')
        dosage_start_date = request.args.get('dosage_start_date')
        dosage_end_date = request.args.get('dosage_end_date')
        time_until_next_dose = request.args.get('time_until_next_dose')
        dosage_frequency_unit = request.args.get('dosage_frequency_unit')
        dosage_frequency = request.args.get('dosage_frequency')
        dosage_number = request.args.get('dosage_number')
        id = db.add_medication(name, manufacturer_name, dosage_start_date, dosage_end_date, time_until_next_dose, dosage_frequency_unit, dosage_frequency, dosage_number)
        db.run_query(f'UPDATE users SET med_ids="{db.get_medicines_for_user(username)}" WHERE username="{username}"')
        return 'true'
    else:
        return 'false'

# authentication, username and hashed password
@app.route('/api/v1/auth')
def auth():
    username = request.args.get('username')
    hash = request.args.get('hash')
    if db.get_hash(username) == hash:
        return 'true'
    else:
        return 'false'
    

@app.route('/api/v1/get_medicines_for_user')
def get_medicines_for_user():
    username = request.args.get('username')
    return db.get_medicines_for_user(username)
    
# run lookups.get_interactions on every possible pair of medicines for a user
@app.route('/api/v1/get_interactions_for_user')
def get_interactions_for_user():
    username = request.args.get('username')
    meds = db.get_medicines_for_user(username)
    interactions = []
    for i in range(len(meds)):
        for j in range(i+1, len(meds)):
            interactions.append(lookups.get_interactions(meds[i][1], meds[j][1]))
    while 'no interactions found!' in interactions: interactions.remove('no interactions found!')
    return interactions

if __name__ == '__main__':
    app.run(debug=True, port=8080)
