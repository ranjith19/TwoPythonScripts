#       launch_script.py
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
import paramiko
import time
import connection_script


def main():
        first_run=1
        change_status=0
        count=0
	try:
	   while True:
                        print """---------- time:%s----------"""%(time.strftime("%H:%M:%S, %d %b %Y", time.gmtime()))
			
			try:#trying to call Sync_script.py for syncronising local DB 
				print 'synchronising local db'
				change_status=Sync_script.main()
				if change_status!=0:
                                        last_update_time=now
				
			except:
				logging.error('error synchronisng:'+time.strftime("%H:%M:%S, %d %b %Y", time.gmtime())+str(sys.exc_info()))

			if change_status==0 :
                                #wait for 2 seconds before syncronising again
                                time.sleep(2)
                        else:
                                count+=1
                        if count==200:
                                count=0
                                ssh= connection_script.connect_to_webserver()
                                cmd='python2.7 /home/pearlwhite85/webapps/django1_2_7/syncscripts/warehouse2webserver/delete_items_without_pics.py '
                                stdin,stdout,stderr= ssh.exec_command(cmd)
                                print std
                                ssh.close()
                                
	except KeyboardInterrupt:
			print 'exiting now'
			sys.exit()
	except:
			print 'unexpected error'
			raise

if __name__ == "__main__":
    main()
