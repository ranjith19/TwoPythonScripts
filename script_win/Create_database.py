import sqlite3
import settings_script

def create_database():
	connection=sqlite3.connect(settings_script.SQLITE_DB)
	cursor=connection.cursor()
	cursor.execute("create table inv_data (prod_cd char(21) not null unique, whs_num char(8) not null unique, UPDT_DT numeric(8,0), STATUS char(1) not null);")
	connection.commit()
	cursor.close()

create_database()