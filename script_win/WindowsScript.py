import pyodbc #to load the ODBC module.
import paramiko



#defining local database variables
DB_SERVER='{SQL SERVER}' #name of server
SERVER_LOC='localhost'#location of server
DB_NAME='omsdata'#name of database

#Defining ssh connection varaiables
HOST='184.172.207.82'
UNAME='pearlwhite85'
PWD='*data85'


#establishing connections
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=UNAME, password=PWD)

#conncting to locaal database.
CONNECTION_STRING='DRIVER='+DB_SERVER+';SERVER='+SERVER_LOC+';DATABASE='+DB_NAME

db_connection=pyodbc.connect(CONNECTION_STRING) #connection to database

cursor=db_connection.cursor()#defining a cursor for connection

cursor.execute("select * from dbo.inv_data")#Selecting all rows  ####needs work####
row = 
for row in curser:
	s=print row
	print s.type