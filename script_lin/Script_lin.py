import sys
import psycopg2
import settings_script

def insert_script:

def update_script:


conn = psycopg2.connect(settings_script.connection_string)
cur = conn.cursor()



cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")