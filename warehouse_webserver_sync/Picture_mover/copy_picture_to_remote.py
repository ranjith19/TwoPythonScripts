#       copy_picture_to_remote.py
#       
#       Copyright 2011 ranjith19 <ranjith19@gmail.com>
#       
#       This script moves pictures from a directory to the remote machine 
#		if the name of the file matches prod_cd column of
#		inv_data table in MS SQL database
#
#		This script needs connection_script.py  and settings_script.py for working
#		
#		make sure paramiko and pyodbc modules are installed before 
#		running the script
# 		also make sure that the path name provided in the
#		settings_script.py for the remote_script is correct
#		double check the filename


import sys
import sqlite3
import pyodbc
import connection_script
import settings_script
import logging
import re              # regex module
import datetime

def move_file():
	pass
#the main function

def main():
	now= datetime.datetime.now()
	timestamp= now.strftime("%Y%m%d%H%M%S")#getting the timestamp 
	#creating log file
	logging.basicConfig(filename='copy_pictures_to_remote.log',level=logging.DEBUG)
	logging.info('begin at'+timestamp)
	try:
		lite_con,lite_cur=connection_script.connect_to_sqlite()#connect to sqlite3
		ms_con, ms_cur=connection_script.connect_to_mssql()#connect to ms sql
		ssh=connection_script.connect_to_webserver()# connect to unix box
		total_updates=0
		total_inserts=0
		#  picking up the newly updated and inserted data from the sqlite3 DB
		
			# get the data from MS SQL
			ms_query="select prod_cd from inv_data where whs_num='1';"
			ms_cur.execute(ms_query)
			
			for row in ms_cur:
				
			ms_row=ms_cur.fetchone()#fetch the row
			
			row_status=lite_row[1]#variable to identify if the row is newly inserted or updated
			
			
			cmd='python2.7 '+ settings_script.remote_script 
			i=0# a temporary counter
			
			#generating command line arguments        
			cmd,i=add_to_cmd(cmd,i,'prod_cd',pass_prod_cd)  
			cmd,i=add_to_cmd(cmd,i,'whs_num',ms_row.whs_num)
			cmd,i=add_to_cmd(cmd,i,'in_stock',ms_row.in_stock)
			cmd,i=add_to_cmd(cmd,i,'lastrcv_qty',ms_row.lastrcv_qty)
			cmd,i=add_to_cmd(cmd,i,'lastrcv_dt',ms_row.lastrcv_dt)
			cmd,i=add_to_cmd(cmd,i,'price_base',ms_row.price_base)
			cmd,i=add_to_cmd(cmd,i,'frt_cus',ms_row.frt_cus)
			cmd,i=add_to_cmd(cmd,i,'prod_duty',ms_row.prod_duty)
			cmd,i=add_to_cmd(cmd,i,'handl_fee',ms_row.handl_fee)
			cmd,i=add_to_cmd(cmd,i,'misc_fee',ms_row.misc_fee)
			cmd,i=add_to_cmd(cmd,i,'lt_sl_dt',ms_row.lt_sl_dt)
			cmd,i=add_to_cmd(cmd,i,'vendor',ms_row.vendor)
			cmd,i=add_to_cmd(cmd,i,'lst_order',ms_row.lst_order)
			cmd,i=add_to_cmd(cmd,i,'ord_dt',ms_row.ord_dt)
			cmd,i=add_to_cmd(cmd,i,'stk_ind',ms_row.stk_ind)
			cmd,i=add_to_cmd(cmd,i,'back_qty',ms_row.back_qty)
			cmd,i=add_to_cmd(cmd,i,'order_qty',ms_row.order_qty)
			cmd,i=add_to_cmd(cmd,i,'on_order_qty',ms_row.on_order_qty)
			cmd,i=add_to_cmd(cmd,i,'wip_qty',ms_row.wip_qty)
			cmd,i=add_to_cmd(cmd,i,'rma_qty',ms_row.rma_qty)
			cmd,i=add_to_cmd(cmd,i,'water_qty',ms_row.water_qty)
			cmd,i=add_to_cmd(cmd,i,'ordersize',ms_row.ordersize)
			cmd,i=add_to_cmd(cmd,i,'minstock',ms_row.minstock)
			cmd,i=add_to_cmd(cmd,i,'inv_loc',ms_row.inv_loc)
			cmd,i=add_to_cmd(cmd,i,'unit_color',ms_row.unit_color)
			cmd,i=add_to_cmd(cmd,i,'class_cd',ms_row.class_cd)
			cmd,i=add_to_cmd(cmd,i,'descrip','"'+ms_row.descrip+'"')
			cmd,i=add_to_cmd(cmd,i,'def_unit',ms_row.def_unit)
			cmd,i=add_to_cmd(cmd,i,'updt_dt',ms_row.updt_dt)
			cmd,i=add_to_cmd(cmd,i,'phyc_dt',ms_row.phyc_dt)
			cmd,i=add_to_cmd(cmd,i,'image_nm',ms_row.image_nm)
			cmd,i=add_to_cmd(cmd,i,'oem_cd',ms_row.oem_cd)
			cmd,i=add_to_cmd(cmd,i,'alt_cd',ms_row.alt_cd)
			cmd,i=add_to_cmd(cmd,i,'updt_by',ms_row.updt_by)
			cmd,i=add_to_cmd(cmd,i,'currency_cost',ms_row.currency_cost)
			cmd,i=add_to_cmd(cmd,i,'cost_factor',ms_row.cost_factor)
			cmd=re.sub(' +',' ',cmd)
			
			#executing the linux script
			stdin, stdout, stderr = ssh.exec_command(cmd)
			
			if stdout:
				stdoutput=stdout.read()
				print stdoutput
				prod_cd=re.sub(r'\s', '', ms_row.prod_cd)
				print stdoutput.find(prod_cd) ,  stdoutput.find('created')
				
				#check if the output has the string inserted in it just to be sure. 
                                #The script there should not be modified without unless it gives update in the same way
				if (stdoutput.find(prod_cd)!=-1 and  stdoutput.find('created')!=-1):
                                        
                                        lite_cur.execute("update inv_data_bk set  status='Y' where prod_cd =%s"%('"' +lite_row[0]+'"'))
                                        rc=lite_cur.rowcount
                                        if rc==1:
                                                lite_con.commit()
                                                logging.info('created/updated table:'+lite_row[0])
                                                print 'created/updated table:'+lite_row[0]
                                        else:
                                                print 'unexpected rownum',rc
				else:
					print stdoutput
					logging.info('unable to update status:'+lite_row[0]+stdoutput)
					print 'unable ',stdoutput
				

			if stderr:
							print stderr.read()
		#close connections        
		lite_con.close()
		ms_con.close()
		ssh.close()
		print 'total updates tried:',total_updates
		print 'total inserts tried:',total_inserts
	except KeyboardInterrupt:
                sys.exit()
		raise
	except:
		print 'Unexpected error:',sys.exc_info()
		raise

if __name__ == "__main__":
    main()
