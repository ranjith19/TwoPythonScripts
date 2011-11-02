#       db_pass_script.py
#       
#       Copyright 2011 ranjith19 <ranjith19@gmail.com>
#       
#       This script extracts new and changed data based on 
#		results of Sync_script.py from Microsoft SQL server,
#		and inserts database into the unix box
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

#this function creates the argument for the script on the unix box
def add_to_cmd(cmd,i,arg, val):
        
	if type(val)==str :  #deals wiht strings
		if re.match("[^A-Za-z0-9]",val):
				pass
		else:
				cmd=cmd+"--"+arg+"="+val+"  "
		i=i+1
		
		return cmd,i
	else:	#deals with integers and floats
		fval=float(val)
		ival=int(fval)
		if fval==0:
				pass
		else:
				if fval-ival==0: #checking if it is a integer
						cmd=cmd+"--"+arg+"="+str(ival)+"  "
				else:
						cmd=cmd+"--"+arg+"="+str(fval)+"  "
				
		i=i+1
		return cmd,i

#the main function

def main():
	now= datetime.datetime.now()
	timestamp= now.strftime("%Y%m%d%H%M%S")#getting the timestamp 
	#creating log file
	logging.basicConfig(filename='db_pass_script.log')
	logging.info('begin at'+timestamp)
	try:
		lite_con,lite_cur=connection_script.connect_to_sqlite()#connect to sqlite3
		ms_con, ms_cur=connection_script.connect_to_mssql()#connect to ms sql
		ssh=connection_script.connect_to_webserver()# connect to unix box
		total_tries=0
		
		#  picking up the newly updated and inserted data from the sqlite3 DB
		lite_cur.execute("select prod_cd,status from inv_data_bk where status<>'Y' and status<>'V';")
		lite_rows=lite_cur.fetchall()
		for lite_row in lite_rows:
			pass_prod_cd=lite_row[0]
			if pass_prod_cd.find('('):
				pass_prod_cd=pass_prod_cd.replace('(','_-')
			if pass_prod_cd.find(')'):
					pass_prod_cd=pass_prod_cd.replace(')','-_')
					pass_prod_cd=str(pass_prod_cd)
			# get the data from MS SQL
			ms_qry="SELECT i.prod_cd prod_cd,\
				  i.descrip,\
				  i.image_nm pics,\
				  i.class_cd class_cd,\
				  i.sales_cost sales_cost,				  \
				  d.in_stock in_stock,\
				  d.order_qty order_qty\
				FROM omsdata.dbo.inv i,\
				  omsdata.dbo.inv_data d\
				WHERE d.prod_cd=i.prod_cd\
				AND i.prod_cd='%s';"%(lite_row[0])
			ms_cur.execute(ms_qry)
			ms_row=ms_cur.fetchone()#fetch the row
			row_status=lite_row[1]#variable to identify if the row is newly inserted or updated
			cmd='python2.7 '+ settings_script.remote_script 
			i=0# a temporary counter
			print row_status, 'row status'
			if row_status=='D':
				cmd,i=add_to_cmd(cmd,i,'program_mode','delete')
				cmd,i=add_to_cmd(cmd,i,'prod_cd',pass_prod_cd)
				
			else:
				if row_status=='N':
					cmd,i=add_to_cmd(cmd,i,'program_mode','insert')
				elif row_status=='U':
					cmd,i=add_to_cmd(cmd,i,'program_mode','update')
				#generating command line arguments        
				cmd,i=add_to_cmd(cmd,i,'prod_cd',pass_prod_cd)  
				cmd,i=add_to_cmd(cmd,i,'in_stock',ms_row.in_stock)
				cmd,i=add_to_cmd(cmd,i,'sales_cost',ms_row.sales_cost)
				cmd,i=add_to_cmd(cmd,i,'order_qty',ms_row.order_qty)
				cmd,i=add_to_cmd(cmd,i,'class_cd',ms_row.class_cd)
				cmd,i=add_to_cmd(cmd,i,'descrip','"'+ms_row.descrip+'"')
				cmd=re.sub(' +',' ',cmd)
				
			#executing the linux script
			stdin, stdout, stderr = ssh.exec_command(cmd)
			if stdout:
				stdoutput=stdout.read()
				print stdoutput
				
				prod_cd=re.sub(r'\s', '', ms_row.prod_cd)
				#print stdoutput.find(prod_cd) ,  stdoutput.find('created')
				
				
				
				#check if the output has the string inserted in it just to be sure. 
                                #The script there should not be modified without unless it gives update in the same way
				if (stdoutput.find(prod_cd)!=-1 and  stdoutput.find('created')!=-1):
					lite_cur.execute("update inv_data_bk set  status='Y' where prod_cd =%s"%('"' +lite_row[0]+'"'))
					rc=lite_cur.rowcount
					if rc==1:
							lite_con.commit()
							total_tries+=1
							logging.info('created/updated table:'+lite_row[0])
							print 'created/updated table:'+lite_row[0]
					else:
							print 'unexpected rownum',rc
				elif (stdoutput.find(prod_cd)!=1) and (stdoutput.find('removed from products and products categories')!=-1):
					lite_cur.execute("update inv_data_bk set  status='V' where prod_cd =%s"%('"' +lite_row[0]+'"'))
					rc=lite_cur.rowcount
					if rc==1:
							lite_con.commit()
							total_tries+=1
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
		print 'total number of updates, inserts  tried:',total_tries
		
		return total_tries
	except KeyboardInterrupt:
                sys.exit()
		raise
	except:
		print 'Unexpected error:',sys.exc_info()
		raise

if __name__ == "__main__":
    main()
