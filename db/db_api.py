import pathlib
import sqlite3
import pandas as pd
from datetime import datetime
import time

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

def insert_sensor(name, anomaly, value, date, id_trace, id):
    sensor = (name, anomaly, value, date, id_trace, id)
    statement = f'INSERT INTO sensors (name, anomaly, value, date, id_trace, id) VALUES (?, ?, ?, ?, ?, ?);'
    cur = DB_CONN.cursor()
    cur.execute(statement, sensor)
    DB_CONN.commit()
    return cur.lastrowid

def select_people():
    statement = f'SELECT * FROM people;'
    df = pd.read_sql_query(statement, DB_CONN)
    return df

def insert_person(name, surname, birth_year, disabled, id):
    person = (name, surname, birth_year, disabled, id)
    statement = f'INSERT INTO people (name, surname, birth_year, disabled, id) VALUES (?, ?, ?, ?, ?);'
    cur = DB_CONN.cursor()
    cur.execute(statement, person)
    DB_CONN.commit()
    return cur.lastrowid

def select_traces(id_person):
    statement = f'SELECT * FROM traces WHERE id_person = {id_person};'
    df = pd.read_sql_query(statement, DB_CONN)
    return df

def insert_trace(name, date, id_person, id):
    trace = (name, date, id_person, id)
    statement = f'INSERT INTO traces (name, date, id_person, id) VALUES (?, ?, ?, ?);'
    cur = DB_CONN.cursor()
    cur.execute(statement, trace)
    DB_CONN.commit()
    return cur.lastrowid

def traces_count():
    statement = f'SELECT count() FROM traces;'
    cur = DB_CONN.cursor()
    cur.execute(statement)
    DB_CONN.commit()
    return cur.fetchall()

def delete_traces(oldest_time):
    statement = f'DELETE FROM traces WHERE date < {oldest_time};'
    cur = DB_CONN.cursor()
    cur.execute(statement)
    DB_CONN.commit()
    return cur.fetchall()

def delete_sensors(oldest_time):
    statement = f'DELETE FROM sensors WHERE date < {oldest_time};'
    cur = DB_CONN.cursor()
    cur.execute(statement)
    DB_CONN.commit()
    return cur.fetchall()

def get_time():
    return int(datetime.now().timestamp())

if __name__ == "__main__":

    count = 0
    while True:
        time.sleep(1)
        res = insert_trace('Trace name', get_time(), 0, count)
        res = insert_sensor('L1', 0, 3.14, get_time(), count, count)
        count = count + 1
        res = delete_traces(get_time() - 5)
        res = delete_sensors(get_time() - 5)
        res = select_sensor()
        print('SENSORS:', res)
        res = select_traces(0)
        print('TRACES:', res)
        print('COUNT:', count)


# # TESTING PEOPLE TABLE
#     res = select_people()
#     print('PEOPLE:\n', res)
#     res = insert_person('Adam', 'Czajka', '1998', 0, 0)
#     print('INSERT PERSON:\n', res, sep=' ')
#     res = select_people()
#     print('PEOPLE:\n', res)
#     print()

# TESTING TRACES TABLE
    # res = select_traces(0)
    # print('TRACES:\n', res)
    # res = insert_trace('Trace name 0', get_time(), 0, 0)
    # print('INSERT TRACE:\n', res, sep=' ')
    # res = insert_trace('Trace name 1', get_time(), 1, 1)
    # print('INSERT TRACE:\n', res, sep=' ')
    # res = select_traces(1)
    # print('TRACES:\n', res)
    # print()


# # TESTING SENSORS TABLE
#     res = select_sensor()
#     print('SENSORS:\n', res)
#     res = insert_sensor('L1', 0, 3.14, 0, 0)
#     print('INSERT SENSOR:\n', res, sep=' ')
#     res = select_sensor()
#     print('SENSORS:\n', res)
#     print()






