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
    run_query('INSERT INTO medications VALUES ("2", "Ciprofloxacin", "Camber Pharmaceuticals, Inc.", "2021-01-01", "2021-05-01", "1", "hour", "12", "2")')

if __name__ == '__main__':
    reset_db()
