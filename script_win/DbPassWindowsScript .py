import sys
import sqlite3
import pyodbc
import connection_script
import logging
import re              # regex module
import 

logging.basicConfig(filename='db_sync.log',level=logging.DEBUG)

lite_con,lite_cur=connection_script.connect_to_sqlite()

ssh=connection_script.connect_to_webserver()

lite_cur.execute("select prod_cd,whs_num,in_stock,lastrcv_qty,lastrcv_dt,price_base,frt_cus,prod_duty,handl_fee,misc_fee,avg_cost,lt_sl_dt,vendor,lst_order,ord_dt,stk_ind,back_qty,order_qty,on_order_qty,wip_qty,rma_qty,water_qty,ordersize,minstock,inv_loc,unit_color,class_cd,descrip,def_unit,updt_dt,phyc_dt,image_nm,oem_cd,alt_cd,updt_by,currency_cost,cost_factor  from inv_data_bk where status='U' or status='N';")
lite_rows=lite_cur.fetchall()
print 'total rows:',len(lite_rows)
for lite_row in lite_rows:
	row_status=lite_row.status
	if status=='N':
		cmd='python2.7 /home/pearlwhite85/test_proj/script_lin/arguments.py  --program_mode=insert '
	elif status == 'U':
		cmd='python2.7 /home/pearlwhite85/test_proj/script_lin/arguments.py  --program_mode=update '
	
	i=0
	def add_to_cmd(cmd,i,arg, val):
		if type(val)==str:
			if re.match("[^A-Za-z0-9]",val):
				print "not parsing a null string argument"+arg
			else:
				cmd=cmd+"--"+arg+"="+val+"  "
			i=i+1
			#print i,':',cmd
			return cmd,i
		else:
			fval=float(val)
			ival=int(fval)
			if fval==0:
				print "not parsing a zero as argument"+arg
			else:
				if fval-ival==0:
					cmd=cmd+"--"+arg+"="+str(ival)+"  "
				else:
					cmd=cmd+"--"+arg+"="+str(fval)+"  "
				
			i=i+1
			#print i,':',cmd
			return cmd,i
		
	cmd,i=add_to_cmd(cmd,i,'prod_cd',lite_row.prod_cd)  
	cmd,i=add_to_cmd(cmd,i,'whs_num',lite_row.whs_num)
	cmd,i=add_to_cmd(cmd,i,'in_stock',lite_row.in_stock)
	cmd,i=add_to_cmd(cmd,i,'lastrcv_qty',lite_row.lastrcv_qty)
	cmd,i=add_to_cmd(cmd,i,'lastrcv_dt',lite_row.lastrcv_dt)
	cmd,i=add_to_cmd(cmd,i,'price_base',lite_row.price_base)
	cmd,i=add_to_cmd(cmd,i,'frt_cus',lite_row.frt_cus)
	cmd,i=add_to_cmd(cmd,i,'prod_duty',lite_row.prod_duty)
	cmd,i=add_to_cmd(cmd,i,'handl_fee',lite_row.handl_fee)
	cmd,i=add_to_cmd(cmd,i,'misc_fee',lite_row.misc_fee)
	cmd,i=add_to_cmd(cmd,i,'lt_sl_dt',lite_row.lt_sl_dt)
	cmd,i=add_to_cmd(cmd,i,'vendor',lite_row.vendor)
	cmd,i=add_to_cmd(cmd,i,'lst_order',lite_row.lst_order)
	cmd,i=add_to_cmd(cmd,i,'ord_dt',lite_row.ord_dt)
	cmd,i=add_to_cmd(cmd,i,'stk_ind',lite_row.stk_ind)
	cmd,i=add_to_cmd(cmd,i,'back_qty',lite_row.back_qty)
	cmd,i=add_to_cmd(cmd,i,'order_qty',lite_row.order_qty)
	cmd,i=add_to_cmd(cmd,i,'on_order_qty',lite_row.on_order_qty)
	cmd,i=add_to_cmd(cmd,i,'wip_qty',lite_row.wip_qty)
	cmd,i=add_to_cmd(cmd,i,'rma_qty',lite_row.rma_qty)
	cmd,i=add_to_cmd(cmd,i,'water_qty',lite_row.water_qty)
	cmd,i=add_to_cmd(cmd,i,'ordersize',lite_row.ordersize)
	cmd,i=add_to_cmd(cmd,i,'minstock',lite_row.minstock)
	cmd,i=add_to_cmd(cmd,i,'inv_loc',lite_row.inv_loc)
	cmd,i=add_to_cmd(cmd,i,'unit_color',lite_row.unit_color)
	cmd,i=add_to_cmd(cmd,i,'class_cd',lite_row.class_cd)
	cmd,i=add_to_cmd(cmd,i,'descrip','"'+lite_row.descrip+'"')
	cmd,i=add_to_cmd(cmd,i,'def_unit',lite_row.def_unit)
	cmd,i=add_to_cmd(cmd,i,'updt_dt',lite_row.updt_dt)
	cmd,i=add_to_cmd(cmd,i,'phyc_dt',lite_row.phyc_dt)
	cmd,i=add_to_cmd(cmd,i,'image_nm',lite_row.image_nm)
	cmd,i=add_to_cmd(cmd,i,'oem_cd',lite_row.oem_cd)
	cmd,i=add_to_cmd(cmd,i,'alt_cd',lite_row.alt_cd)
	cmd,i=add_to_cmd(cmd,i,'updt_by',lite_row.updt_by)
	cmd,i=add_to_cmd(cmd,i,'currency_cost',lite_row.currency_cost)
	cmd,i=add_to_cmd(cmd,i,'cost_factor',lite_row.cost_factor)
	cmd=re.sub(' +',' ',cmd)
	print cmd
	stdin, stdout, stderr = ssh.exec_command(cmd)
	
	if stdout:
			lite_cur.execute("update inv_data set  status='Y' where prod_cd ='" +prod_cd+"';")
			lite_con.commit()
			print stdout.read()
	print 'yes ', prod_cd
	if stderr:
			print stderr.read()
	break
lite_con.close()
ms_con.close()
ssh.close()
