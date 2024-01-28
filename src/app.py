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

@app.route('/api/v1/adduser')
def adduser():
    username = request.args.get('username')
    full_name = request.args.get('full_name')
    hash = request.args.get('hash')
    db.add_user(username, full_name, hash)
    return 'true'

@app.route('/api/v1/add')
def add():
    username = request.args.get('username')
    hash = request.args.get('hash')
    if db.get_hash(username) == hash:
        name = request.args.get('name')
        manufacturer_name = request.args.get('manufacturer_name')
        dosage_start_date = request.args.get('dosage_start_date')
        dosage_end_date = request.args.get('dosage_end_date')
        dosage_frequency_unit = request.args.get('dosage_frequency_unit')
        dosage_frequency = request.args.get('dosage_frequency')
        total = db.calc_total_doses(dosage_start_date, dosage_end_date, dosage_frequency_unit, dosage_frequency)
        print(f"db.add_medication('{name}', '{manufacturer_name}', '{dosage_start_date}', '{dosage_end_date}', '{dosage_frequency_unit}', {dosage_frequency}, {total}, 0)")
        id = db.add_medication(name, manufacturer_name, dosage_start_date, dosage_end_date, dosage_frequency_unit, int(dosage_frequency), total, 0)
        db.add_id_to_user(username, id)
        return 'true'
    else:
        return 'false'
    

# delete a medication from a user's list
# /api/v1/delete?username=jdoe&hash=5f4dcc3b5aa765d61d8327deb882cf99&id=1
@app.route('/api/v1/delete')
def delete():
    username = request.args.get('username')
    hash = request.args.get('hash')
    if db.get_hash(username) == hash:
        id = request.args.get('id')
        db.run_query(f'DELETE FROM medications WHERE id={id}')
        med_ids = db.run_query(f'SELECT med_ids FROM users WHERE username="{username}"')[0][0]
        med_ids = med_ids.split(',')
        med_ids.remove(id)
        med_ids = ','.join(med_ids)
        db.run_query(f'UPDATE users SET med_ids="{med_ids}" WHERE username="{username}"')
        return 'true'
    else:
        return 'false'

# mark a dose as taken
# /api/v1/take?username=jdoe&hash=5f4dcc3b5aa765d61d8327deb882cf99&id=1
@app.route('/api/v1/take')
def take():
    username = request.args.get('username')
    hash = request.args.get('hash')
    if db.get_hash(username) == hash:
        id = request.args.get('id')
        total_doses = db.run_query(f'SELECT total_doses FROM medications WHERE id={id}')[0][0]
        if taken_doses == total_doses: 
            pass
        else:
            taken_doses = db.run_query(f'SELECT taken_doses FROM medications WHERE id={id}')[0][0]
            taken_doses += 1
            db.run_query(f'UPDATE medications SET taken_doses={taken_doses} WHERE id={id}')
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
    hash = request.args.get('hash')
    if db.get_hash(username) == hash: return db.get_medicines_for_user(username)
    else: return 'INVALID HASH'

# run lookups.get_interactions on every possible pair of medicines for a user
@app.route('/api/v1/get_interactions_for_user')
def get_interactions_for_user():
    username = request.args.get('username')
    hash = request.args.get('hash')
    if db.get_hash(username) == hash:
        meds = db.get_medicines_for_user(username)
        interactions = []
        for i in range(len(meds)):
            for j in range(i+1, len(meds)):
                interactions.append(lookups.get_interactions(meds[i][1], meds[j][1]))
        while 'no interactions found!' in interactions: interactions.remove('no interactions found!')
        return interactions
    else:
        return 'INVALID HASH'

if __name__ == '__main__':
    app.run(debug=True, port=8080)
