#       warehouse2webserver_lin.py
#       
#       Copyright 2011 ranjith19 <ranjith19@gmail.com>
#       
#       this script updates the database on unix box
#
#		This script needs connection_script.py  and settings_script.py for working
#		
#		make sure psycopg2 is installed before 
#		running the script
#
# 		also make sure that the path name provided in the
#		settings_script.py for the remote_script is correct
#		double check the filename

import MySQLdb#deals with the mysql db
from optparse import OptionParser# for dealing with script's arguments
import re#for dealing regex
import function_script#contains all the functions needed
import logging# for logfiles
import datetime#for generating timestamp
import sys

def main():
	#defining logfile
	logging.basicConfig(filename='/home/pearlwhite85/webapps/django1_2_7/syncscripts/warehouse2webserver/warehouse2webserver.log',level=logging.DEBUG)
	
	#logging.info('beginning operation'+str(datetime.datetime.now()))
	#defining command line options
	parser = OptionParser(usage="usage: %prog [options] ", version="%prog 1.0")
	#parser.add_option( "--program_mode",dest="program_mode",default="insert")
	parser.add_option( "--prod_cd",dest="prod_cd",default=' ')
	parser.add_option( "--whs_num", dest="whs_num", default=' ')
	parser.add_option( "--in_stock", dest="in_stock", type="float",default=0.0)
	parser.add_option( "--lastrcv_qty", dest="lastrcv_qty", type="float",default=0.0)
	parser.add_option( "--lastrcv_dt", dest="lastrcv_dt",type="int",default=0)
	parser.add_option( "--price_base", dest="price_base",type="float",default=0.0)
	parser.add_option( "--frt_cus", dest="frt_cus",type="float",default=0.0)
	parser.add_option( "--prod_duty", dest="prod_duty",type="float",default=0.0)
	parser.add_option( "--handl_fee", dest="handl_fee",type="float",default=0.0)
	parser.add_option( "--misc_fee", dest="misc_fee",type="float",default=0.0)
	parser.add_option( "--avg_cost", dest="avg_cost",type="float",default=0.0)
	parser.add_option( "--lt_sl_dt", dest="lt_sl_dt",type="int",default=0)
	parser.add_option( "--vendor", dest="vendor",default=' ')
	parser.add_option( "--lst_order", dest="lst_order",type="float",default=0.0)
	parser.add_option( "--ord_dt", dest="ord_dt",type="int",default=0)
	parser.add_option( "--stk_ind", dest="stk_ind",default=' ')
	parser.add_option( "--back_qty", dest="back_qty",type="float",default=0.0)
	parser.add_option( "--order_qty", dest="order_qty",type="float",default=0.0)
	parser.add_option( "--on_order_qty", dest="on_order_qty",type="float",default=0.0)
	parser.add_option( "--wip_qty", dest="wip_qty",type="float",default=0.0)
	parser.add_option( "--rma_qty", dest="rma_qty",type="float",default=0.0)
	parser.add_option( "--water_qty", dest="water_qty",type="float",default=0.0)
	parser.add_option( "--ordersize", dest="ordersize",type="float",default=0.0)
	parser.add_option( "--minstock", dest="minstock",type="float",default=0.0)
	parser.add_option( "--inv_loc", dest="inv_loc",default=' ')
	parser.add_option( "--unit_color", dest="unit_color",default=' ')
	parser.add_option( "--class_cd", dest="class_cd",default=' ')
	parser.add_option( "--descrip", dest="descrip",default=' ')
	parser.add_option( "--def_unit", dest="def_unit",default=' ')
	parser.add_option( "--updt_dt", dest="updt_dt",type="int",default=0)
	parser.add_option( "--phyc_dt", dest="phyc_dt",type="float",default=0.0)
	parser.add_option( "--image_nm", dest="image_nm",default=' ')
	parser.add_option( "--oem_cd", dest="oem_cd",default=' ')
	parser.add_option( "--alt_cd", dest="alt_cd",default=' ')
	parser.add_option( "--updt_by", dest="updt_by",default=' ')
	parser.add_option( "--currency_cost", dest="currency_cost",type="float",default=0.0)
	parser.add_option( "--cost_factor", dest="cost_factor",type="float",default=0.0)
	try:#obtain options
		(options, args) = parser.parse_args()
	except:
		print 'pass options correctly'
		raise
	try:#connecting to linx database
		dbcon,dbcur=function_script.connect_to_db()
	except:
		print 'error while connecting'
		raise
	#print 'program mode  tried:',options.program_mode
	
	dbcur.execute("select * from pearlwhite85.inv_data_bk where prod_cd ='" +options.prod_cd+"';")
	dbrow=dbcur.fetchone()
	if dbrow:
		print 'droppting row:',options.prod_cd
		try:
			delete_query="delete from pearlwhite85.inv_data_bk where prod_cd ='" +options.prod_cd+"';"
			#logging.info("deleting row before for update:"+options.prod_cd+' at '+timestamp)
			dbcur.execute(delete_query)
			print delete_query
		except:
			logging.error('error:'+delete_query)
			#logging.error('Error while delete at '+str(datetime.datetime.now())+':unexpected error at '+str(sys.exc_info())+'  prod cd='+options.prod_cd)
			print 'unexpected error while dropping row before updating', options.prod_cd
			raise



	query="""\
	INSERT INTO inv_data_bk \
	VALUES\
	(\
	%s,%s,%s,%s,%s,%s,\
	%s,%s,%s,%s,%s,%s,\
	%s,%s,%s,%s,%s,%s,\
	%s,%s,%s,%s,%s,%s,\
	%s,%s,%s,%s,%s,%s,\
	%s,%s,%s,%s,%s,%s,%s\
	)"""
	if options.prod_cd.find('_-'):
		#print options.prod_cd
		options.prod_cd=options.prod_cd.replace('_-','(')
		options.prod_cd=options.prod_cd.replace('-_',')')
			
	insert_query=query%( "'"+options.prod_cd+"'",
		"'"+options.whs_num+"'",
		options.in_stock,
		options.lastrcv_qty,
		options.lastrcv_dt,
		options.price_base,
		options.frt_cus	,
		options.prod_duty,
		options.handl_fee ,
		options.misc_fee ,
		options.avg_cost ,
		options.lt_sl_dt ,
		"'"+options.vendor +"'"	,
		options.lst_order ,
		options.ord_dt,
		"'"+options.stk_ind+"'" ,
		options.back_qty ,
		options.order_qty ,
		options.on_order_qty,
		options.wip_qty ,
		options.rma_qty ,
		options.water_qty ,
		options.ordersize ,
		options.minstock ,
		"'"+options.inv_loc+"'" ,
		"'"+options.unit_color+"'" ,
		"'"+options.class_cd+"'",
		"'"+options.descrip+"'",
		"'"+options.def_unit+"'" ,
		options.updt_dt ,
		options.phyc_dt ,
		"'"+options.image_nm +"'",
		"'"+options.oem_cd 	+"'",
		"'"+options.alt_cd 	+"'",
		"'"+options.updt_by  +"'",
		options.currency_cost,
		options.cost_factor,
		)
	#print insert_query
	try:
		#logging.info('inserting row'+options.prod_cd)
		print 'creating row:'
		dbcur.execute(insert_query)#creating row
		print 'created  row',options.prod_cd
	except:
		logging.error('error while inserting:' +options.prod_cd+str(sys.exc_info()))
		print 'error while creating',sys.exc_info()
	dbcon.commit()
	dbcon.close()#closing connection

if __name__ == "__main__":
    main()