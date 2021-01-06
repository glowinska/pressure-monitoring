import pathlib
import sqlite3
import pandas as pd
from datetime import datetime
import time
import json
from time import time,sleep
import requests
import threading

DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath("DatabaseName2.db").resolve()
#conn = None
# try:
#     conn = sqlite3.connect(str(DB_FILE))
# except Error as err:
#     print(err)

def select_sensor(conn, id_trace):
    statement = f'SELECT * FROM sensors WHERE id_trace = {id_trace};'
    df = pd.read_sql_query(statement, conn)
    return df

def insert_sensor(conn, name, anomaly, value, date, id_trace, id):
    sensor = (name, anomaly, value, date, id_trace, id)
    statement = f'INSERT INTO sensors (name, anomaly, value, date, id_trace, id) VALUES (?, ?, ?, ?, ?, ?);'
    cur = conn.cursor()
    cur.execute(statement, sensor)
    conn.commit()
    return cur.lastrowid

def select_sensor_for_trace(conn, id_trace, name):
    statement = f'SELECT * FROM sensors WHERE id_trace = {id_trace} AND name ="{name}";'
    df = pd.read_sql_query(statement, conn)
    return df

def select_people(conn):
    statement = f'SELECT * FROM people;'
    df = pd.read_sql_query(statement, conn)
    return df

def select_people_by_id(conn):
    #con = sqlite3.connect(str(DB_FILE))
    statement = f'SELECT * FROM people WHERE rowid = "{id}"";'
    df = pd.read_sql_query(statement, conn)
    return df

def insert_person(conn, name, surname, birth_year, disabled, id):
    person = (name, surname, birth_year, disabled, id)
    statement = f'INSERT INTO people (name, surname, birth_year, disabled, id) VALUES (?, ?, ?, ?, ?);'
    cur = conn.cursor()
    cur.execute(statement, person)
    conn.commit()
    return cur.lastrowid

def select_traces(conn, id_person):
    statement = f'SELECT * FROM traces WHERE id_person = {id_person};'
    df = pd.read_sql_query(statement, conn)
    return df

def insert_trace(conn, name, date, id_person, id):
    trace = (name, date, id_person, id)
    statement = f'INSERT INTO traces (name, date, id_person, id) VALUES (?, ?, ?, ?);'
    cur = conn.cursor()
    cur.execute(statement, trace)
    conn.commit()
    return cur.lastrowid

def traces_count(conn):
    statement = f'SELECT count() FROM traces;'
    cur = conn.cursor()
    cur.execute(statement)
    conn.commit()
    return cur.fetchall()

def delete_traces(conn, oldest_time):
    statement = f'DELETE FROM traces WHERE date < {oldest_time};'
    cur = conn.cursor()
    cur.execute(statement)
    conn.commit()
    return cur.fetchall()

def delete_sensors(conn, oldest_time):
    statement = f'DELETE FROM sensors WHERE date < {oldest_time};'
    cur = conn.cursor()
    cur.execute(statement)
    conn.commit()
    return cur.fetchall()

def get_time():
    return int(datetime.now().timestamp())

def get_request(url):
    sleep(2)
    r = requests.get(url)
    return r.json()
    

def get_data():
    monitor1, monitor2, monitor3, monitor4, monitor5, monitor6 = {}, {}, {}, {}, {}, {}
    conn = None
    try:
        conn = sqlite3.connect(str(DB_FILE))
    except Error as err:
        print(err)
    print("XD")
    delete_sensors(conn, get_time())
    print("lll")
    count = 0
    while True:
        #print(monitor1)
        timerrr = get_time()
        print(type(monitor1))
        monitor1 = get_request('http://tesla.iem.pw.edu.pl:9080/v2/monitor/1')
        trace = monitor1['trace']
        # def insert_trace(name, date, id_person, id):
        insert_trace(conn, trace['name'], timerrr, 1, trace['id'])
        # def insert_sensor(name, anomaly, value, date, id_trace, id):
        sensors = trace['sensors']
        for sensor in sensors:
            count = count + 1
            insert_sensor(conn, sensor['name'], sensor['anomaly'], sensor['value'], timerrr, trace['id'], count)
        delete_sensors(conn, timerrr - 5)
        delete_traces(conn, timerrr - 5)

if __name__ == "__main__":
    t = threading.Thread(target=get_data, args=[])
    t.start()
    # delete_sensors(get_time())
    # count = 0
    # while True:
    #     #print(monitor1)
    #     timerrr = get_time()
    #     print(type(monitor1))
    #     monitor1 = get_request('http://tesla.iem.pw.edu.pl:9080/v2/monitor/1')
    #     trace = monitor1['trace']
    #     # def insert_trace(name, date, id_person, id):
    #     insert_trace(trace['name'], timerrr, 1, trace['id'])
    #     # def insert_sensor(name, anomaly, value, date, id_trace, id):
    #     sensors = trace['sensors']
    #     for sensor in sensors:
    #         count = count + 1
    #         insert_sensor(sensor['name'], sensor['anomaly'], sensor['value'], timerrr, trace['id'], count)
    #     delete_sensors(timerrr - 5)
    #     delete_traces(timerrr - 5)
        # select_traces(1)
        # select_sensor(1)
        
#    while True:
#        time.sleep(1)
#        res = insert_trace('Trace name', get_time(), 0, count)
#        res = insert_sensor('L1', 0, 3.14, get_time(), count, count)
#        count = count + 1
#        res = delete_traces(get_time() - 5)
#        res = delete_sensors(get_time() - 5)
#        res = select_sensor(3)
#        print('SENSORS:', res)
#        res = select_traces(0)
#        print('TRACES:', res)
#        print('COUNT:', count)


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






