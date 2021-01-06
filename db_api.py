import pathlib
import sqlite3
import pandas as pd
DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath("DatabaseName.db").resolve()
DB_CONN = None
try:
    DB_CONN = sqlite3.connect(str(DB_FILE))
except Error as err:
    print(err)

def select_sensor():
    statement = f'SELECT * FROM sensors;'
    df = pd.read_sql_query(statement, DB_CONN)
    return df

def insert_sensor(name, anomaly, value, id_trace, id):
    sensor = (name, anomaly, value, id_trace, id)
    statement = f'INSERT INTO sensors (name, anomaly, value, id_trace, id) VALUES (?, ?, ?, ?, ?);'
    cur = DB_CONN.cursor()
    cur.execute(statement, sensor)
    DB_CONN.commit()
    return cur.lastrowid

def select_people():
    statement = f'SELECT * FROM people;'
    df = pd.read_sql_query(statement, DB_CONN)
    return df

def select_people_by_id(id):
    statement = f'SELECT * FROM people WHERE id = {id};'
    df = pd.read_sql_query(statement, DB_CONN)
    return df

def insert_person(name, surname, birth_year, disabled, id):
    person = (name, surname, birth_year, disabled, id)
    statement = f'INSERT INTO people (name, surname, birth_year, disabled, id) VALUES (?, ?, ?, ?, ?);'
    cur = DB_CONN.cursor()
    cur.execute(statement, person)
    DB_CONN.commit()
    return cur.lastrowid

def select_traces():
    statement = f'SELECT * FROM traces;'
    df = pd.read_sql_query(statement, DB_CONN)
    return df

def insert_trace(name, date, id_person, id):
    trace = (name, date, id_person, id)
    statement = f'INSERT INTO traces (name, date, id_person, id) VALUES (?, ?, ?, ?);'
    cur = DB_CONN.cursor()
    cur.execute(statement, trace)
    DB_CONN.commit()
    return cur.lastrowid


if __name__ == "__main__":
# TESTING SENSORS TABLE
    res = select_sensor()
    print('SENSORS:\n', res)
    #res = insert_sensor('L1', 0, 3.14, 0, 0)
    print('INSERT SENSOR:\n', res, sep=' ')
    res = select_sensor()
    print('SENSORS:\n', res)
    print()

# TESTING PEOPLE TABLE
    res = select_people()
    print('PEOPLE:\n', res)
    #res = insert_person('Adam', 'Czajka', '1998', 0, 1)
    print('INSERT PERSON:\n', res, sep=' ')
    res = select_people_by_id(1)
    print('PEOPLE:\n', res)
    print()

# TESTING TRACES TABLE
    res = select_traces()
    print('TRACES:\n', res)
    #res = insert_trace('Trace name', 'date', 0, 1)
    print('INSERT TRACE:\n', res, sep=' ')
    res = select_traces()
    print('TRACES:\n', res)
    print()




