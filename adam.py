import pathlib
import sqlite3
import pandas as pd

DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath("DatabaseName.db").resolve()

def create_tab_sensors_if_not_exists(id, id_trace, name, anomaly, value):
    conn = sqlite3.connect(str(DB_FILE))
    df = "hihi"
    #statement = f'CREATE TABLE IF NOT EXISTS sensors (id PRIMARY KEY NOT NULL, id_trace TEXT NOT NULL, name TEXT, anomaly INTEGER, value REAL);'
    #df = pd.read_sql_query(statement, conn)
    return df

def select_sensors():
    conn = sqlite3.connect(str(DB_FILE))
    statement = f'SELECT * FROM sensors;'
    df = pd.read_sql_query(statement, conn)
    return df

def select_people():
    conn = sqlite3.connect(str(DB_FILE))
    statement = f'SELECT * FROM people;'
    df = pd.read_sql_query(statement, conn)
    return df

def select_traces():
    conn = sqlite3.connect(str(DB_FILE))
    statement = f'SELECT * FROM traces;'
    df = pd.read_sql_query(statement, conn)
    return df
    
def insert_sensor(name, anomaly, value, id_trace):
    conn = sqlite3.connect(str(DB_FILE))
    sensor = (name, anomaly, value, id_trace)
    statement = f'INSERT INTO sensors (name, anomaly, value, id_trace) VALUES (?, ?, ?, ?);'
    cur = conn.cursor()
    cur.execute(statement, sensor)
    conn.commit()
    return cur.lastrowid

if __name__ == "__main__":
    res = select_sensors()
    print(res)
    aa = insert_sensor("a", "b", "c", 16)
    res = select_sensors()
    print(res)
