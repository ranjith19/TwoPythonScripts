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
import sqlite3
import settings_script
import connection_script
import paramiko

def main():
	try:
        
                     
		confirm_char=raw_input( 'Are you sure? This will delete all data in temporary database (Y/N)')
		if confirm_char=='Y':
                         
			create_query="""CREATE TABLE inv_data_bk(\
			prod_cd       CHAR(21) NOT NULL PRIMARY KEY,\
			whs_num       CHAR(8),\
			in_stock      NUMERIC(21,6),\
			lastrcv_qty   NUMERIC(21,6)   ,\
			lastrcv_dt    NUMERIC(8,0)   ,\
			price_base    NUMERIC(21,6)   ,\
			frt_cus       NUMERIC(21,6)   ,\
			prod_duty     NUMERIC(21,6)   ,\
			handl_fee     NUMERIC(21,6)   ,\
			misc_fee      NUMERIC(21,6)   ,\
			avg_cost      NUMERIC(21,6)   ,\
			lt_sl_dt      NUMERIC(8,0)   ,\
			vendor        CHAR(10) ,\
			lst_order     NUMERIC(21,6) ,\
			ord_dt        NUMERIC(8,0)   ,\
			stk_ind       CHAR(1),\
			back_qty      NUMERIC(21,6)   ,\
			order_qty     NUMERIC(21,6)   ,\
			on_order_qty  NUMERIC(21,6)   ,\
			wip_qty       NUMERIC(21,6)   ,\
			rma_qty       NUMERIC(21,6)   ,\
			water_qty     NUMERIC(21,6)   ,\
			ordersize     NUMERIC(21,6)   ,\
			minstock      NUMERIC(21,6)   ,\
			inv_loc       CHAR(20),\
			unit_color    CHAR(11),\
			class_cd      CHAR(20),\
			descrip       CHAR(61),\
			def_unit      CHAR(2),\
			updt_dt       NUMERIC(8,0)   ,\
			phyc_dt       NUMERIC(21,6)   ,\
			image_nm      CHAR(80),\
			oem_cd        CHAR(20),\
			alt_cd        CHAR(20),\
			updt_by       CHAR(8),\
			currency_cost NUMERIC(21,6)   ,\
			cost_factor   NUMERIC(21,6)   ,\
			status CHAR(1));"""
                        def delete_database():
                            connection, cursor= connection_script.connect_to_sqlite()
                            cursor.execute("""DROP TABLE inv_data_bk;""")
                            cursor.close()
                            connection.close()
                            
                        def create_database():
                            connection, cursor= connection_script.connect_to_sqlite()
                            cursor.execute(create_query)
                            connection.commit()
                            cursor.close()
                            connection.close()
			

			try:
				try:
					delete_database()
					print 'dropped table inv_data_bk'
				except:# should not fail unless its the first time
					print 'unable to delete'
					pass
				create_database()
				print 'created table inv_data_bk'
			except:
				print 'Error:unexpected error\n',sys.exc_info()
			
		else:
			print 'exiting without doing anything'

	except:
		print 'Error:unexpected error',sys.exc_info()
                	
if __name__ == "__main__":
    main()
