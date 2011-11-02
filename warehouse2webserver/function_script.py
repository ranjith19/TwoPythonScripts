#       function_script.py
#       
#       Copyright 2011 ranjith19 <ranjith19@gmail.com>
#       
#       this script connects to  db
#		This file needs settings script to run properly
#		please install python-mysql library before running this file

import MySQLdb#library  connecting to my sql db
import settings_script

def connect_to_db():#connects to db
	conn = MySQLdb.connect(user='%s'%(settings_script.UNAME), passwd="%s"%(settings_script.PWD),db="%s"%(settings_script.UNAME))
	cur = conn.cursor()
	return conn, cur
	
