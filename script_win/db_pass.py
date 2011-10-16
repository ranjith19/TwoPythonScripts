import sys
import sqlite3
import pyodbc
import connection_script
import logging

logging.basicConfig(filename='db_sync.log',level=logging.DEBUG)

ms_con, ms_cur=connection_script.connect_to_mssql()
lite_con,lite_cur=connection_script.connect_to_sqlite()

ssh=connection_script.connect_to_webserver()

lite_cur.execute("select * from inv_data")# where status = 'N'")
lite_rows=lite_cur.fetchall()
print 'rowwount',len(lite_rows)
i=0
for lite_row in lite_rows:
        i=i+1
        print i
	status=lite_row[3]
	if status=='N':
		prod_cd = lite_row[0]
		whs_num = lite_row[1]
		updt_dt = lite_row[2]
		ms_query="select * from inv_data where prod_cd ='" +prod_cd+"';"
		ms_cur.execute(ms_query)
		ms_row=ms_cur.fetchone()
		text_row=''
		for i in range(0,len(ms_row)):
			text_row=text_row+str(ms_row[i])+' '
		stdin, stdout, stderr = ssh.exec_command('python2.7 /home/pearlwhite85/test_proj/test.py '+text_row)
		
		if stdout:
			lite_cur.execute("update inv_data set  status='Y' where prod_cd ='" +prod_cd+"';")
			lite_con.commit()
			print stdout.read()
                        print 'yes ', prod_cd
lite_con.close()
ms_con.close()
ssh.close()
