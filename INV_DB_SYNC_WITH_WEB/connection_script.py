#       connection_script.py
#       
#       Copyright 2011 ranjith19 <ranjith19@gmail.com>
#       
#       This script defines the functions to connect to Microsoft SQL server,
#		SQLITE3 database and the unix box
#		
#       This file needs settings_script.py for functioning properly

import paramiko #for ssh connection to UNIX box
import pyodbc #for ssh connection to MS SQL SERVER
import sqlite3 #for connection to Sqlite 3 DB
import sys 
import settings_script #has the user names and passwords



def connect_to_mssql(): #connects to MS SQL DB
	CONNECTION_STRING='DRIVER='+settings_script.MS_SERVER+';SERVER='+settings_script.MS_SERVER_LOC+';DATABASE='+settings_script.MS_DB_NAME
        connection=pyodbc.connect(CONNECTION_STRING) #connection to database
        cursor=connection.cursor()#defining a cursor for connection
        return connection, cursor

def connect_to_sqlite(): #connects to SQLITE3 DB
	connection=sqlite3.connect(settings_script.SQLITE_DB)
	cursor=connection.cursor()
	return connection, cursor
	
def connect_to_webserver(): #connects to Unix box
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(settings_script.HOST, username=settings_script.UNAME, password=settings_script.PWD)
	return ssh



