import pyodbc
import sqlite3
import connection_script

ms_con, ms_cur=connection_script.connect_to_mssql()
lite_con,lite_cur=connection_script.connect_to_sqlite()
lite_cur.execute("select prod_cd from inv_data_bk order by prod_cd");
rows=lite_cur.fetchall()
errors=0
done=0

for row in rows:
	prod_cd=row[0]
	ms_cur.execute("select sales_cost from inv where prod_cd='%s';"%(prod_cd))
	ms_row=ms_cur.fetchone()
	lite_cur.execute("update inv_data_bk set sales_cost=%s where prod_cd='%s';"%(ms_row.sales_cost,prod_cd))
	if lite_cur.rowcount:
                done+=1
                print 'affected rows:',lite_cur.rowcount
		print str("item=%s, cost=%s, rows done=%s"%(prod_cd,ms_row.sales_cost,float(done*100)/7106))
		
	else:
		errors+=1
		print str("error item=%s, cost=%s"%(prod_cd,ms_row.sales_cost))
lite_con.commit()
lite_con.close()
ms_con.close()
