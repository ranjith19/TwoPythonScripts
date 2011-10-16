import sys
import sqlite3
import settings_script
import connection_script

def create_database():
	connection, cursor= connection_script.connect_to_sqlite()
	cursor.execute("create table inv_data (prod_cd char(21) not null , whs_num char(8) not null , UPDT_DT numeric(8,0), STATUS char(1) not null);")
	connection.commit()
	cursor.close()
	connection.close()

try:
	create_database()
except sqlite3.OperationalError:
	print 'Error:table already exists',sys.exc_info()[0]
except:
	print 'Error:unexpected error',sys.exc_info()[0]
	