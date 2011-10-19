import os
import datetime
import logging
import subprocess





while True:
	now= datetime.datetime.now()
	timestamp= now.strftime("%Y%m%d%H%M%S")
	for filename in os.listdir("."):
		if filename.endswith('.log'):
			newname=timestamp+filename+'ed'
			os.rename(filename,newname)
	logging.basicConfig(filename='run_script_log',level=logging.DEBUG)
	try:
                print 'synchronising local db'
		child = subprocess.call("c:\Python27\python.exe  Sync_script.py", shell=True)
		
	except:
		logging.error('error synchronisng:'+timestamp)
	try:
                print 'synchronising remote db'
		child = subprocess.call("c:\Python27\python.exe  db_pass_script.py", shell=True)
	except:
		logging.error('error passing:'+timestamp)
