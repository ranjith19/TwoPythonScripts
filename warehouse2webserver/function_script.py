import MySQLdb
import settings_script

def connect_to_db():
	conn = MySQLdb.connect(user='%s'%(settings_script.UNAME), passwd="%s"%(settings_script.PWD),db="%s"%(settings_script.UNAME))
	cur = conn.cursor()
	return conn, cur
	
def insert_script():
	return 0
	
def update_script():
	return 0