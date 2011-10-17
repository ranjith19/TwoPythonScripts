import sys
import sqlite3
import pyodbc
import connection_script
import logging
import re              # regex module

logging.basicConfig(filename='db_sync.log',level=logging.DEBUG)

ms_con, ms_cur=connection_script.connect_to_mssql()
lite_con,lite_cur=connection_script.connect_to_sqlite()

ssh=connection_script.connect_to_webserver()

lite_cur.execute("select * from inv_data")# where status = 'N'")
lite_rows=lite_cur.fetchall()



print 'rowcount',len(lite_rows)
for lite_row in lite_rows:
        status=lite_row[3]
        if status=='N':
			prod_cd = lite_row[0]
			whs_num = lite_row[1]
			updt_dt = lite_row[2]
			ms_query="select prod_cd,whs_num,in_stock,lastrcv_qty,LASTRCV_DT,price_base,FRT_CUS,PROD_DUTY,HANDL_FEE,MISC_FEE,AVG_COST,LT_SL_DT,VENDOR,LST_ORDER,ORD_DT,STK_IND,BACK_QTY,ORDER_QTY,ON_ORDER_QTY,WIP_QTY,RMA_QTY,WATER_QTY,ORDERSIZE,MINSTOCK,INV_LOC,UNIT_COLOR,CLASS_CD,DESCRIP,DEF_UNIT,UPDT_DT,PHYC_DT,IMAGE_NM,OEM_CD,ALT_CD,UPDT_BY,CURRENCY_COST,COST_FACTOR  from inv_data where prod_cd ='" +prod_cd+"';"
			ms_cur.execute(ms_query)
			ms_row=ms_cur.fetchone()
			print len(ms_row)
			#print ms_row
			cmd=''
			print 'prod cd',ms_row.prod_cd
			prod
			for i in range(0,len(ms_row)):
				if  type(ms_row[i])==str:
					if re.match("[^A-Za-z]",ms_row[i]):
						print "not printing a null string"
					else:
						print type(ms_row[i]), ms_row[i]
					
				else:
					print type(float(ms_row[i]))   ,ms_row[i]
			
			
			break
			stdin, stdout, stderr = ssh.exec_command('python2.7 /home/pearlwhite85/test_proj/arguments.py '+text_row)
			
			if stdout:
					lite_cur.execute("update inv_data set  status='Y' where prod_cd ='" +prod_cd+"';")
					lite_con.commit()
					print stdout.read()
			print 'yes ', prod_cd
			break
lite_con.close()
ms_con.close()
ssh.close()
