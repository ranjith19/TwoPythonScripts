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
#defining functions

#establishing connections
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=UNAME, password=PWD)

#conncting to locaal database.
CONNECTION_STRING='DRIVER='+DB_SERVER+';SERVER='+SERVER_LOC+';DATABASE='+DB_NAME
db_connection=pyodbc.connect(CONNECTION_STRING) #connection to database
cursor=db_connection.cursor()#defining a cursor for connection

cursor.execute("select * from dbo.inv_data")#Selecting all rows  ####needs work####
row=cursor.fetchone()
text_row=''
for i in range(0,len(row)):
	text_row=text_row+str(row[i])+' '

stdin, stdout, stderr = ssh.exec_command('python2.7 /home/pearlwhite85/test_proj/test.py '+text_row)
print stdout.read()
print stderr.read()
