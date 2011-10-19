import sys
import sqlite3
import settings_script
import connection_script

def create_database():
	connection, cursor= connection_script.connect_to_sqlite()
	cursor.execute("""DROP TABLE inv_data_bk;""")
	cursor.execute()
	connection.commit()
	cursor.close()
	connection.close()

try:
	create_database()
except sqlite3.OperationalError:
	print 'Error:table already exists',sys.exc_info()[0]
except:
	print 'Error:unexpected error',sys.exc_info()[0]
	
