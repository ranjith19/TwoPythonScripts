import os
import datetime
import logging
import subprocess




try:
       while True:
                now= datetime.datetime.now()
                timestamp= now.strftime("%Y%m%d%H%M%S")
                
                try:
                        print 'synchronising local db'
                        subprocess.call("c:\Python27\python.exe  Sync_script.py", shell=True)
                        
                except:
                        logging.error('error synchronisng:'+timestamp)
                try:
                        print 'synchronising remote db'
                        subprocess.call("c:\Python27\python.exe  db_pass_script.py", shell=True)
                except:
                        logging.error('error passing:'+timestamp)
except KeyboardInterrupt:
        print 'exiting now'
except:
        print 'unexpected error'
