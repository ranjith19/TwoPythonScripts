#       Sync_script.py#       #       Copyright 2011 ranjith19 <ranjith19@gmail.com>#       #       This script syncronises the MS SQL AND SQLITE3 DB,#		#		#       This file needs connection_script.py settings_script.py for functioning properly#		edit the settings in settings_script.pyimport sysimport sqlite3import pyodbcimport connection_scriptimport loggingimport datetimeimport reimport datetimedef main():	now= datetime.datetime.now()	timestamp= now.strftime("%Y%m%d%H%M%S")	#log file creation	logging.basicConfig(filename='logfile\\Sync_script.log',level=logging.DEBUG)	logging.info('Begin at :'+timestamp)	try:		total_updates=0		total_inserts=0		#connect to Databases		ms_con, ms_cur=connection_script.connect_to_mssql()		lite_con,lite_cur=connection_script.connect_to_sqlite()				ms_cur.execute("select count(*) as c from dbo.inv_data where whs_num= '1';")		ms_row_count=ms_cur.fetchone()# total rows in MSSQL db		#fetching the MSSQL DB		ms_cur.execute("select prod_cd,whs_num,in_stock,lastrcv_qty,lastrcv_dt,price_base,frt_cus,prod_duty,handl_fee,misc_fee,avg_cost,lt_sl_dt,vendor,lst_order,ord_dt,stk_ind,back_qty,order_qty,on_order_qty,wip_qty,rma_qty,water_qty,ordersize,minstock,inv_loc,unit_color,class_cd,descrip,def_unit,updt_dt,phyc_dt,image_nm,oem_cd,alt_cd,updt_by,currency_cost,cost_factor  from inv_data where whs_num='1' and prod_cd like '%';")				for ms_row in ms_cur:#do for all rows                        			prod_cd = ms_row.prod_cd			ms_row.descrip=ms_row.descrip.replace('\"','')			#general structure of query for insert/update			query="\			INSERT INTO inv_data_bk \			VALUES\			(\			%s,%s,%s,%s,%s,%s,\			%s,%s,%s,%s,%s,%s,\			%s,%s,%s,%s,%s,%s,\			%s,%s,%s,%s,%s,%s,\			%s,%s,%s,%s,%s,%s,\			%s,%s,%s,%s,%s,%s,%s,'%c'\			);"			#insert query			insert_query=query%( "'"+ms_row.prod_cd+"'",			'"'+ms_row.whs_num+'"',			ms_row.in_stock,			ms_row.lastrcv_qty,			ms_row.lastrcv_dt,			ms_row.price_base,			ms_row.frt_cus	,			ms_row.prod_duty,			ms_row.handl_fee ,			ms_row.misc_fee ,			ms_row.avg_cost ,			ms_row.lt_sl_dt ,			'"'+ms_row.vendor +'"'	,			ms_row.lst_order ,			ms_row.ord_dt,			'"'+ms_row.stk_ind+'"' ,			ms_row.back_qty ,			ms_row.order_qty ,			ms_row.on_order_qty,			ms_row.wip_qty ,			ms_row.rma_qty ,			ms_row.water_qty ,			ms_row.ordersize ,			ms_row.minstock ,			'"'+ms_row.inv_loc+'"' ,			'"'+ms_row.unit_color+'"' ,			'"'+ms_row.class_cd+'"',			'"'+ms_row.descrip+'"',			'"'+ms_row.def_unit+'"' ,			ms_row.updt_dt ,			ms_row.phyc_dt ,			'"'+ms_row.image_nm +'"',			'"'+ms_row.oem_cd 	+'"',			'"'+ms_row.alt_cd 	+'"',			'"'+ms_row.updt_by  +'"',			ms_row.currency_cost,			ms_row.cost_factor,			'N'			)			#update query			update_query=query%( "'"+ms_row.prod_cd+"'",			'"'+ms_row.whs_num+'"',			ms_row.in_stock,			ms_row.lastrcv_qty,			ms_row.lastrcv_dt,			ms_row.price_base,			ms_row.frt_cus	,			ms_row.prod_duty,			ms_row.handl_fee ,			ms_row.misc_fee ,			ms_row.avg_cost ,			ms_row.lt_sl_dt ,			'"'+ms_row.vendor +'"'	,			ms_row.lst_order ,			ms_row.ord_dt,			'"'+ms_row.stk_ind+'"' ,			ms_row.back_qty ,			ms_row.order_qty ,			ms_row.on_order_qty,			ms_row.wip_qty ,			ms_row.rma_qty ,			ms_row.water_qty ,			ms_row.ordersize ,			ms_row.minstock ,			'"'+ms_row.inv_loc+'"' ,			'"'+ms_row.unit_color+'"' ,			'"'+ms_row.class_cd+'"',			'"'+ms_row.descrip+'"',			'"'+ms_row.def_unit+'"' ,			ms_row.updt_dt ,			ms_row.phyc_dt ,			'"'+ms_row.image_nm +'"',			'"'+ms_row.oem_cd 	+'"',			'"'+ms_row.alt_cd 	+'"',			'"'+ms_row.updt_by  +'"',			ms_row.currency_cost,			ms_row.cost_factor,			'U'			)						sqlite_query="select prod_cd,whs_num,in_stock,lastrcv_qty,lastrcv_dt,price_base,frt_cus,prod_duty,handl_fee,misc_fee,avg_cost,lt_sl_dt,vendor,lst_order,ord_dt,stk_ind,back_qty,order_qty,on_order_qty,wip_qty,rma_qty,water_qty,ordersize,minstock,inv_loc,unit_color,class_cd,descrip,def_unit,updt_dt,phyc_dt,image_nm,oem_cd,alt_cd,updt_by,currency_cost,cost_factor  from inv_data_bk where prod_cd ='" +prod_cd+"';"			#sqlite_query has the string for selecting rows with prod_cd obtained for the current row in MS SQL DB			lite_cur.execute(sqlite_query)			lite_row=lite_cur.fetchone()			if not lite_row:#see if a row exists with that prod_cd				try:					lite_cur.execute(insert_query)#insert if no row found					total_inserts+=1					print('inserted '+prod_cd)				except:					logging.error('Error while insert at '+str(datetime.datetime.now())+':unexpected error at '+str(sys.exc_info()))					logging.error('error: '+insert_query)					print 'error: ',insert_query			elif lite_row:#if row exists				flag=0#variable that flags change				for i in range(0,len(ms_row)):#comparing element by element					if type(ms_row[i])==str:#for string elements                                                                                    						if i!=1 and ms_row[i]!=lite_row[i]:							flag=1							#print 'flag raised str',ms_row[i],' ',lite_row[i]							break						elif 1==i and int(ms_row[i])!=int(lite_row[i]):							flag=1							#print 'flag raised whs_num',ms_row.prod_cd							break					else:#for numbers						if float(ms_row[i])!=float(lite_row[i]):							flag=1							#print 'flag raised float',ms_row[i],' ',lite_row[i]							break				if flag==1:#if flagged					try:						delete_script="delete from inv_data_bk where prod_cd ='" +ms_row.prod_cd+"';"						total_updates+=1						#print delete_script						lite_cur.execute(delete_script)#deleting the row						lite_con.commit()						lite_cur.execute(update_query)#inserting the row						print 'updated', ms_row.prod_cd, 'rows afftected:',lite_cur.rowcount					except:								logging.error('Error while update:'+str(datetime.datetime.now())+'unexpected error at '+prod_cd+str(sys.exc_info()))						logging.error('error: '+insert_query)						print 'error: ',insert_query				#else:						#print 'not updating',prod_cd			lite_con.commit()		lite_cur.execute("select count(*) from inv_data_bk;")#number of rows in temp db		lite_row_count=lite_cur.fetchone()		print 'total rows:',ms_row_count.c		#print 'total rows in secondary db:',lite_row_count[0]						if total_updates!=0 or total_inserts!=0:                        print 'total inserts:',total_inserts                        print 'total updates:',total_updates                                                return total_updates+total_inserts                else :                        print 'no changes in the primary db'                        return 0                		lite_con.close()		ms_con.close()	except KeyboardInterrupt:		print 'exiting now from sync_script'				raise	except:		print 'Unexpected error:',sys.exc_info()		raiseif __name__ == "__main__":    main()