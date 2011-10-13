import pyodbc #to loda the ODBC module.


DB_SERVER='{SQL SERVER}'
SERVER_LOC='localhost'
DB_NAME='omsdata'

CONNECTION_STRING='DRIVER='+DB_SERVER+';SERVER='+SERVER_LOC+';DATABASE='+DB_NAME

db_connection=pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=omsdata') #connection to database
cursor=connection.cursor()#defining a cursor for connection
cursor.execute("select * from dbo.inv_data")#Selecting all rows

