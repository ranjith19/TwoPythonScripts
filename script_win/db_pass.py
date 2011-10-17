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
			ms_query="select prod_cd,whs_num,in_stock,lastrcv_qty,lastrcv_dt,price_base,frt_cus,prod_duty,handl_fee,misc_fee,avg_cost,lt_sl_dt,vendor,lst_order,ord_dt,stk_ind,back_qty,order_qty,on_order_qty,wip_qty,rma_qty,water_qty,ordersize,minstock,inv_loc,unit_color,class_cd,descrip,def_unit,updt_dt,phyc_dt,image_nm,oem_cd,alt_cd,updt_by,currency_cost,cost_factor  from inv_data where prod_cd ='" +prod_cd+"';"
			ms_cur.execute(ms_query)
			ms_row=ms_cur.fetchone()
			print len(ms_row)
			#print ms_row
			cmd='python2.7 /home/pearlwhite85/test_proj/arguments.py '
			print cmd
			i=0
			def add_to_cmd(cmd,i,arg, val):
				if type(val)==str:
					if re.match("[^A-Za-z]^[0-9]",val):
						print "not parsing a null string argument"+arg
					else:
						cmd=cmd+"--"+arg+"="+val+"  "
					i=i+1
					print i,':',cmd
					return cmd,i
				else:
					fval=float(val)
					if fval==0:
						print "not parsing a zero as argument"+arg
					else:
						cmd=cmd+"--"+arg+"="+str(fval)+"  "
					i=i+1
					print i,':',cmd
					return cmd,i
				
			cmd,i=add_to_cmd(cmd,i,'prod_cd',ms_row.prod_cd)  
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
			break
			stdin, stdout, stderr = ssh.exec_command(cmd)
			
			if stdout:
					lite_cur.execute("update inv_data set  status='Y' where prod_cd ='" +prod_cd+"';")
					lite_con.commit()
					print stdout.read()
			print 'yes ', prod_cd
			break
lite_con.close()
ms_con.close()
ssh.close()
