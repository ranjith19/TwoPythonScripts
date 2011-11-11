def validate_qty(name,qty):
	import sys
	import MySQLdb
	HOST="localhost"
	UNAME='pearlwhite85' 
	PWD='eekthecat85'	
	def connect_to_db():#connects to db
		conn = MySQLdb.connect(user='%s'%( UNAME), passwd="%s"%( PWD),db="%s"%( UNAME))
		cur = conn.cursor()
		return conn, cur
	con,cur=connect_to_db()
	qry="select quantity from pearlwhite85.products where sku='%s'"%(name)
	cur.execute(qry)
	row=cur.fetchone()
	db_qty=row[0]
	con.close()
	print db_qty
	if qty>db_qty:		
		return -1
	else:
		return 1
import sys
name=sys.argv[1]
qty=int(sys.argv[2])
print 'validate:',validate_qty(name,qty) 