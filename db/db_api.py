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
    if conn == None:
        conn = sqlite3.connect(str(DB_FILE))
    statement = f'SELECT * FROM sensors WHERE id_trace = {id_trace} AND name ="{name}";'
    df = pd.read_sql_query(statement, conn)
    return df

def select_people(conn):
    statement = f'SELECT * FROM people;'
    df = pd.read_sql_query(statement, conn)
    return df

def select_people_by_id(id):
    conn = sqlite3.connect(str(DB_FILE))
    statement = f'SELECT * FROM people WHERE rowid = {id};'
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
    if conn == None:
        conn = sqlite3.connect(str(DB_FILE))
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

def delete_people(conn):
    statement = f'DELETE FROM people where 1=1;'
    cur = conn.cursor()
    cur.execute(statement)
    conn.commit()
    return cur.fetchall()

def get_time():
    return datetime.now().timestamp()

def get_request(url):
    sleep(0.05)
    r = requests.get(url)
    return r.json()
    
def get_data():
    monitor = {}
    conn = None
    try:
        conn = sqlite3.connect(str(DB_FILE))
    except Error as err:
        print(err)
    get_people(conn)
    delete_sensors(conn, get_time())
    count = 0
    while True:
        timerrr = get_time()
        for monitor_number in range(1, 7):
            monitor = get_request('http://tesla.iem.pw.edu.pl:9080/v2/monitor/'+str(monitor_number))
            trace = monitor['trace']
            newtraceid =  int(str(trace['id']) + str(count))
            insert_trace(conn, trace['name'], timerrr, monitor_number, newtraceid)
            sensors = trace['sensors']
            for sensor in sensors:
                count = count + 1
                insert_sensor(conn, sensor['name'], sensor['anomaly'], sensor['value'], timerrr, newtraceid, count)
            delete_sensors(conn, timerrr - 20)
            delete_traces(conn, timerrr - 20)
            
def get_people(conn):
    delete_people(conn)
    for monitor_number in range(1, 7):
        monitor = get_request('http://tesla.iem.pw.edu.pl:9080/v2/monitor/'+str(monitor_number))
        insert_person(conn, monitor['firstname'], monitor['lastname'], monitor['birthdate'], monitor['disabled'], monitor_number)        
    
if __name__ == "__main__":
    t = threading.Thread(target=get_data, args=[])
    t.start()
    