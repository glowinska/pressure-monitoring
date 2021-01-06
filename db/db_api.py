import pathlib
import sqlite3
import pandas as pd


DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath("DatabaseName.db").resolve()
def create_connection(db_file): 
    """ create a database connection to the 
    SQLite database specified by 
    db_file :param db_file: 
    database file :return: 
    Connection object or None """ 
    
    conn = None 
    try: conn = sqlite3.connect(db_file) 
    except Error as e: 
        print(e) 
    return conn

def get_wind_data(start, end):
    """
    Query wind data rows between two ranges

    :params start: start row id
    :params end: end row id
    :returns: pandas dataframe object
    """

    con = sqlite3.connect(str(DB_FILE))
    statement = f'SELECT Speed, SpeedError, Direction FROM Wind WHERE rowid > "{start}" AND rowid <= "{end}";'
    df = pd.read_sql_query(statement, con)
    return df


def get_wind_data_by_id(id):
    """
    Query a row from the Wind Table

    :params id: a row id
    :returns: pandas dataframe object
    """

    con = sqlite3.connect(str(DB_FILE))
    statement = f'SELECT * FROM Wind WHERE rowid = "{id}";'
    df = pd.read_sql_query(statement, con)
    return df

def create_tab_sensors_if_not_exists(id, id_trace, name, anomaly, value):
 conn = sqlite3.connect(str(DB_FILE))
 statement = f'CREATE TABLE IF NOT EXISTS sensors (id PRIMARY KEY NOT NULL, id_trace TEXT NOT NULL, name TEXT, anomaly INTEGER, value REAL);'
 df = pd.read_sql_query(statement, conn)
 return df
