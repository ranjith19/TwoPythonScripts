#       run_widows_script.py
#       
#       Copyright 2011 ranjith19 <ranjith19@gmail.com>
#       
#       This script calls scripts:
#			1. Sync_script.py for syncronising local DB 
#			2. db_pass_script.py for updating the remote DB
#       This file needs settings_script.py, connection_script.py for functioning properly
import os
import datetime
import logging
import subprocess
import sys
import Sync_script
import db_pass_script



def main():
	try:
	   while True:
			now= datetime.datetime.now()
			timestamp= now.strftime("%Y%m%d%H%M%S")
			
			try:#trying to call Sync_script.py for syncronising local DB 
				print 'synchronising local db'
				Sync_script.main()
				
			except:
				logging.error('error synchronisng:'+timestamp)
			try:#trying to call db_pass_script.py for updating the remote DB 
				print 'synchronising remote db'
				db_pass_script.main()
			except:
				logging.error('error passing:'+timestamp)
	except KeyboardInterrupt:
			print 'exiting now'
			sys.exit()
	except:
			print 'unexpected error'
			raise

if __name__ == "__main__":
    main()
