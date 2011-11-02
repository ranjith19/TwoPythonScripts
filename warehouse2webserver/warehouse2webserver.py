#       warehouse2webserver_lin.py
#       
#       Copyright 2011 ranjith19 <ranjith19@gmail.com>
#       
#       this script updates the database on unix box
#
#		This script needs connection_script.py  and settings_script.py for working
#		
#		make sure MySQLdb is installed before 
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
from warnings import filterwarnings

filterwarnings('ignore', category = MySQLdb.Warning)
def delete_item(con,cur):
	cur.execute("select prod_cd from pearlwhite85.inv where status='D';")
	rows=cur.fetchall()
	for row in rows:
		q="select id from pearlwhite85.products where prod_cd='%s';"%(row[0])
		cur.execute(q)
		id=cur.fetchone()
		if id:
			cur.execute("delete from pearlwhite85.products where id='%s';"%(id[0]))
		
			cur.execute("delete from pearlwhite85.products_categories where product_id='%s';"%(id[0]))
			cur.commit()
			print 'removed from products and products categories:',row[0]
			
def create_or_update_products(con,cur):
	cur.execute("select  prod_cd, in_stock, order_qty, sales_cost, class_cd, descrip from pearlwhite85.inv where status='N' ;")
	i=0
	rows = cur.fetchall()
	for row in rows:
		
		flag=None
		i+=1		
		Vsku=row[0]
		Vquantity=row[1]-row[2]-10
		if Vquantity<0:
			Vquantity=0
		Vprice=float(row[3])*(1.35)
		Vname=row[4]+' ('+Vsku+')'
		Vcat=row[4]
		Vdesc=row[5]		
		Vimage='images/products/main/'+Vsku+'.jpg'
		Vthumb='images/products/thumbnails/'+Vsku+'.jpg'
		
		
		cur.execute("select * from pearlwhite85.products where sku='%s'"%(Vsku))
		product_row=cur.fetchone()
		
		if product_row:
			flag='U'
		else:
			flag='N'
		
		#print Vsku, Vname
		
		if flag=='U':
			try:
				uqry="""update pearlwhite85.products set  price=%s, quantity=%s, description="%s", updated_at=sysdate() where sku='%s' """%(Vprice,Vquantity,Vsku, Vdesc)
				
				cur.execute(uqry)
				print 'updated row', Vname, Vsku
				con.commit()
				
				#updating categories table
				selqry="select id from pearlwhite85.products where sku='%s';"%(Vsku)
				cur.execute(selqry)
				selrow=cur.fetchone()
				product_id=selrow[0]
				
				catqry="select id from pearlwhite85.categories where name='%s';" %(Vcat)
				cur.execute(catqry)
				catrow=cur.fetchone()
				
				if catrow:
					cat_id=catrow[0]
				else:
					catqry="insert into pearlwhite85.categories  (name, slug, description, is_active, created_at, updated_at) values ('%s','%s','%s',1,sysdate(),sysdate());"%(Vcat, Vcat, Vcat)
					cur.execute(catqry)
					con.commit()
					catqry="select id from pearlwhite85.categories where name='%s'"%(Vcat)
					cur.execute(catqry)
					catrow2=cur.fetchone()
					cat_id=catrow2[0]
				print 'prod id, cat_id:',product_id, cat_id
				linkqry="select * from pearlwhite85.products_categories where product_id=%s and category_id=%s;"%(product_id, cat_id)
				cur.execute(linkqry)
				linkrow=cur.fetchone()	
				if linkrow:
					pass
				else:
					linkqry="insert into pearlwhite85.products_categories (product_id, category_id) values(%s,%s);"%(product_id, cat_id)
					cur.execute(linkqry)
				con.commit()
			except:
				print 'unexpected error when updating products table at:', Vname, Vsku
				raise
		elif flag=='N':
			try:
				iqry="insert into pearlwhite85.products (name, sku, price, quantity, description, is_active, created_at, updated_at,image,thumbnail,image_caption) values  ('%s','%s',%s,%s,'%s', 1, sysdate(),sysdate(),'%s','%s','%s'); "%(Vname,Vsku,Vprice,Vquantity,Vdesc,Vimage,Vthumb,Vsku)
				cur.execute(iqry)
				con.commit()
				print 'created row', Vname, Vsku
				
				#updating categories table
				selqry="select id from pearlwhite85.products where sku='%s';"%(Vsku)
				cur.execute(selqry)
				selrow=cur.fetchone()
				product_id=selrow[0]
				
				catqry="select id from pearlwhite85.categories where name='%s';" %(Vcat)
				cur.execute(catqry)
				catrow=cur.fetchone()
				
				if catrow:
					cat_id=catrow[0]
				else:
					catqry="insert into pearlwhite85.categories  (name, slug, description, is_active, created_at, updated_at) values ('%s','%s','%s',1,sysdate(),sysdate());"%(Vcat, Vcat, Vcat)
					cur.execute(catqry)
					con.commit()
					catqry="select id from pearlwhite85.categories where name='%s'"%(Vcat)
					cur.execute(catqry)
					catrow2=cur.fetchone()
					cat_id=catrow2[0]
				print 'prod id, cat_id:',product_id, cat_id
				linkqry="select * from pearlwhite85.products_categories where product_id=%s and category_id=%s;"%(product_id, cat_id)
				cur.execute(linkqry)
				linkrow=cur.fetchone()	
				if linkrow:
					pass
				else:
					linkqry="insert into pearlwhite85.products_categories (product_id, category_id) values(%s,%s);"%(product_id, cat_id)
					cur.execute(linkqry)
				con.commit()
			except:
				print 'unexpected error when updating products table at:', Vname, Vsku
				raise
		else:
			print 'Unknown flag:',flag
		
		yqry="update pearlwhite85.inv set status='Y' where prod_cd='%s';"%(Vsku)
		#print yqry
		cur.execute(yqry)
		if cur.rowcount:
			print 'affected rows:', cur.rowcount
		con.commit()
			
	return i
	
	

def main():
	#defining logfile
	logging.basicConfig(filename='/home/pearlwhite85/webapps/django1_2_7/syncscripts/warehouse2webserver/warehouse2webserver.log',level=logging.DEBUG)
	
	#logging.info('beginning operation'+str(datetime.datetime.now()))
	#defining command line options
	parser = OptionParser(usage="usage: %prog [options] ", version="%prog 1.0")
	parser.add_option( "--program_mode",dest="program_mode",default="insert")
	parser.add_option( "--prod_cd",dest="prod_cd",default=' ')
	parser.add_option( "--in_stock", dest="in_stock", type="float",default=0.0)
	parser.add_option( "--sales_cost", dest="sales_cost",type="float",default=0.0)
	parser.add_option( "--order_qty", dest="order_qty",type="float",default=0.0)
	parser.add_option( "--class_cd", dest="class_cd",default=' ')
	parser.add_option( "--descrip", dest="descrip",default=' ')
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
	if options.prod_cd.find('_-'):
		#print options.prod_cd
		options.prod_cd=options.prod_cd.replace('_-','(')
		options.prod_cd=options.prod_cd.replace('-_',')')
	prod_cd=options.prod_cd
	
	dbcur.execute("select * from pearlwhite85.inv where prod_cd ='" +options.prod_cd+"';")
	dbrow=dbcur.fetchone()
	if options.program_mode=='delete':
		if dbrow:
			delete_qry="update pearlwhite85.inv set status='D' where prod_cd='%s';"%(options.prod_cd)
			dbcur.execute(delete_qry)
			dbcon.commit()
			delete_item(dbcon,dbcur)
			print "deleted %s from products"%(options.prod_cd)
	
	else:			
		if dbrow:
			print 'droppting row:',options.prod_cd
			try:
				delete_query="delete from pearlwhite85.inv where prod_cd ='" +options.prod_cd+"';"
				#logging.info("deleting row before for update:"+options.prod_cd+' at '+timestamp)
				dbcur.execute(delete_query)
				print options.prod_cd ,' deleted'
			except:
				logging.error('error:'+delete_query)
				#logging.error('Error while delete at '+str(datetime.datetime.now())+':unexpected error at '+str(sys.exc_info())+'  prod cd='+options.prod_cd)
				print 'unexpected error while dropping row before updating', options.prod_cd
				raise

		query="INSERT INTO inv\
			VALUES('%s',%s,%s,%s,'%s','%s','%s',sysdate());"
			
		insert_query=query%(prod_cd,
								options.in_stock,
								options.sales_cost,
								options.order_qty,
								options.class_cd,
								options.descrip,
								'N')

		#print insert_query
		try:
			#logging.info('inserting row'+options.prod_cd)
			print 'creating row:'
			dbcur.execute(insert_query)#creating row
			print 'created  row',options.prod_cd
			dbcon.commit()
			
			
			
		except:
			logging.error('error while inserting:' +options.prod_cd+str(sys.exc_info()))
			print 'error while creating',sys.exc_info()
	
	create_or_update_products(dbcon,dbcur)
	dbcon.close()#closing connection
	

if __name__ == "__main__":
    main()