# python functions to interact with the sqlite3 database
import sqlite3
import tools

# run query on database
def run_query(query):
    conn = sqlite3.connect('dosewise.db')
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
    conn.commit()
    conn.close()
    return result

# reset database
def reset_db():
    run_query('DROP TABLE IF EXISTS users')
    run_query('DROP TABLE IF EXISTS medications')

    # create users table
    run_query('CREATE TABLE users (username TEXT, full_name TEXT, hash TEXT, med_ids TEXT)') # med_ids is a comma separated list of medication ids that belong to the user
    # add test user jane Doe
    run_query('INSERT INTO users VALUES ("jdoe", "Jane Doe", "5f4dcc3b5aa765d61d8327deb882cf99", "2,3,4")')

    # create medications table, ids should be an integer
    
    run_query('CREATE TABLE medications (id INTEGER, name TEXT, manufacturer_name TEXT, dosage_start_date TEXT, dosage_end_date TEXT, dosage_frequency_unit TEXT, dosage_frequency TEXT, dosage_number TEXT)')
    # add test medications

    # every day 2 dose of Ciprofloxacin manufactured by Camber Pharmaceuticals, Inc. from 2021-01-01 to 2021-05-01
    run_query('INSERT INTO medications VALUES (2, "Ciprofloxacin", "Camber Pharmaceuticals, Inc.", "2021-01-01", "2021-05-01", "day", "12", "2")')

    # every 4 hours 1 pill of fluconazole manufactured by Major Pharmaceuticals from 2021-01-01 to 2021-05-01
    run_query('INSERT INTO medications VALUES (3, "fluconazole", "Major Pharmaceuticals", "2021-01-01", "2021-05-01", "hour", "4", "1")')

    # every 12 hours 2 pill of simvastatin manufactured by Dr.Reddys Laboratories Inc from 2021-01-01 to 2021-05-01
    run_query('INSERT INTO medications VALUES (4, "simvastatin", "Dr.Reddys Laboratories Inc", "2021-01-01", "2021-05-01", "hour", "12", "2")')

def get_hash(username):
    return run_query(f'SELECT hash FROM users WHERE username="{username}"')[0][0]

def add_medication(name, manufacturer_name, dosage_start_date, dosage_end_date, dosage_frequency_unit, dosage_frequency, dosage_number):
    id = run_query('SELECT MAX(id) FROM medications')[0][0] + 1
    run_query(f'INSERT INTO medications VALUES ({id}, "{name}", "{manufacturer_name}", "{dosage_start_date}", "{dosage_end_date}", "{dosage_frequency_unit}", "{dosage_frequency}", "{dosage_number}")')
    return id

def add_id_to_user(username, id):
    med_ids = run_query(f'SELECT med_ids FROM users WHERE username="{username}"')[0][0]
    med_ids = med_ids.split(',')
    med_ids.append(str(id))
    print(med_ids)
    med_ids = ','.join(med_ids)
    run_query(f'UPDATE users SET med_ids="{med_ids}" WHERE username="{username}"')    

def get_medicines_for_user(username):
    med_ids = run_query(f'SELECT med_ids FROM users WHERE username="{username}"')[0][0]
    med_ids = med_ids.split(',')
    meds = []
    for med_id in med_ids: meds.append(run_query(f'SELECT * FROM medications WHERE id={med_id}')[0])
    return meds

def add_user(username, full_name, hash):
    run_query(f'INSERT INTO users VALUES ("{username}", "{full_name}", "{hash}", "")')

def calc_total_doses(start_date, end_date, frequency_unit, frequency):
    # first check if the frequency unit is day or hour
    if frequency_unit == 'day':
        days = tools.date_difference_in_days(start_date, end_date)
        return days * frequency
    elif frequency_unit == 'hour':
        hours = tools.date_difference_in_hours(start_date, end_date)
        return hours / frequency

if __name__ == '__main__':
    reset_db()
    # id = add_medication('rand phosphate', 'Roche Laboratories Inc', '2021-01-01', '2021-05-01', 'day', '12', '2')
    # add_id_to_user('jdoe', id)
    # print(get_medicines_for_user('jdoe'))
    
    # every day 2 dose of Ciprofloxacin manufactured by Camber Pharmaceuticals, Inc. from 2021-01-01 to 2021-05-01
    print(calc_total_doses('2021-01-01', '2021-05-01', 'day', 2))
    # every 4 hours 1 pill of fluconazole manufactured by Major Pharmaceuticals from 2021-01-01 to 2021-05-01
    print(calc_total_doses('2021-01-01', '2021-05-01', 'hour', 4))

