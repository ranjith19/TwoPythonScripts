#       create_table.py
#       
#       Copyright 2011 ranjith19 <ranjith19@gmail.com>
#       
#       This script creates the temporary table using
#		SQLITE3 database 
#		
# 		Do not run this file unless you mean to
#       This file needs settings_script.py and connection_script.py for functioning properly 
import sys
import MySQLdb
import function_script

def main():
	try:
		create_query="CREATE TABLE IF NOT EXISTS pearlwhite85.inv (\
		`prod_cd` char(21) NOT NULL,\
		`in_stock` decimal(21,6) default NULL,\
		`sales_cost` decimal(21,6) default NULL,\
		`order_qty` decimal(21,6) default NULL,\
		`class_cd` char(20) default NULL,\
		`descrip` char(61) default NULL,\
		`status` char(1) default NULL,\
		`updated_on` date default NULL,\
		PRIMARY KEY  (`prod_cd`)\
		);"
		create_query=create_query.replace('\t','')


		def create_database():
			connection, cursor= function_script.connect_to_db()
			cursor.execute(create_query)
			connection.commit()
			cursor.close()
			connection.close()


		create_database()
		print 'created table inv'
	except:
		print 'Error:unexpected error\n',sys.exc_info()

	
if __name__ == "__main__":
	main()
