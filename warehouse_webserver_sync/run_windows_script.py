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
import sys
import Sync_script

import time



def main():
        first_run=1
        change_status=0
	try:
	   while True:
			now= datetime.datetime.now()
			last_update_time=now
			timestamp= now.strftime("%Y%m%d%H%M%S")
			
			print """---------- at %s----------"""%(time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()))
			
			try:#trying to call Sync_script.py for syncronising local DB 
				print 'synchronising local db'
				change_status=Sync_script.main()
				
			except:
				logging.error('error synchronisng:'+timestamp)

			if change_status==0 :
                                 
                                print 'last update happened at:',last_update_time, '. Nothing to syncronise now'
                                
                                print 'Waiting for 15 seconds before trying again' 
                                
                                time.sleep(15)
	except KeyboardInterrupt:
			print 'exiting now'
			sys.exit()
	except:
			print 'unexpected error'
			raise

if __name__ == "__main__":
    main()
