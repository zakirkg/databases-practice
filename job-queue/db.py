import psycopg
from psycopg import Connection, Cursor
from psycopg.rows import dict_row

def connect_database():

    connection = psycopg.connect(
        host="localhost",
        port=5432,
        dbname="job_queue",
        user="postgres",
        password="postgres",
    )

    cursor = connection.cursor(
        row_factory = dict_row
    )

    return connection, cursor

def close_connection(connection: Connection, cursor: Cursor):

    cursor.close()
    connection.close()