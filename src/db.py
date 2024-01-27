# python functions to interact with the sqlite3 database
import sqlite3

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
    run_query('INSERT INTO users VALUES ("jdoe", "Jane Doe", "cc3a0280e4fc1415930899896574e118", "1,2")')

    # create medications table
    run_query('CREATE TABLE medications (id TEXT, name TEXT, manufacturer_name TEXT, dosage_start_date TEXT, dosage_end_date TEXT, time_until_next_dose TEXT, dosage_frequency_unit TEXT, dosage_frequency TEXT, dosage_number TEXT)')
    # add test medications

    # every 4 hours 1 pill of OSELTAMIVIR PHOSPHATE manufactured by Camber Pharmaceuticals, Inc. from 2021-01-01 to 2021-05-01
    run_query('INSERT INTO medications VALUES ("1", "OSELTAMIVIR PHOSPHATE", "Camber Pharmaceuticals, Inc.", "2021-01-01", "2021-05-01", "1", "hour", "4", "1")')

    # every 12 hours 2 pill of Ciprofloxacin manufactured by Camber Pharmaceuticals, Inc. from 2021-01-01 to 2021-05-01
    run_query('INSERT INTO medications VALUES ("2", "Ciprofloxacin", "Camber Pharmaceuticals, Inc.", "2021-01-01", "2021-05-01", "1", "day", "12", "2")')

def get_hash(username):
    return run_query(f'SELECT hash FROM users WHERE username="{username}"')[0][0]

def add_medication(name, manufacturer_name, dosage_start_date, dosage_end_date, time_until_next_dose, dosage_frequency_unit, dosage_frequency, dosage_number):
    id = run_query('SELECT MAX(id) FROM medications')[0][0] + 1
    run_query(f'INSERT INTO medications VALUES ("{id}" "{name}", "{manufacturer_name}", "{dosage_start_date}", "{dosage_end_date}", "{time_until_next_dose}", "{dosage_frequency_unit}", "{dosage_frequency}", "{dosage_number}")')
    return id

def get_medicines_for_user(username):
    med_ids = run_query(f'SELECT med_ids FROM users WHERE username="{username}"')[0][0]
    med_ids = med_ids.split(',')
    meds = []
    for med_id in med_ids: meds.append(run_query(f'SELECT * FROM medications WHERE id="{med_id}"')[0])
    return meds



if __name__ == '__main__':
    reset_db()
    print(get_medicines_for_user('jdoe'))
