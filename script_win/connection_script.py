import paramiko
import pyodbc
import pyodbc
import settings_script
import sqlite3
import sys



def connect_to_mssql():
	CONNECTION_STRING='DRIVER='+settings_script.MS_SERVER+';SERVER='+settings_script.MS_SERVER_LOC+';DATABASE='+settings_script.MS_DB_NAME
	connection=pyodbc.connect(CONNECTION_STRING) #connection to database
	cursor=connection.cursor()#defining a cursor for connection
	return connection, cursor

def connect_to_sqlite():
	connection=sqlite3.connect(settings_script.SQLITE_DB)
	cursor=connection.cursor()
	return connection, cursor
	
def connect_to_webserver():
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(settings_script.HOST, username=settings_script.UNAME, password=settings_script.PWD)
	return ssh



