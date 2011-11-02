#       generate_thumbnails.py
#       
#       Copyright 2011 ranjith19 <ranjith19@gmail.com>
#       
#       this script generates thumbnails for the pictures.
#		Number of arguments:2 full filename and and just the filename


import Image
import sys
import logging
logging.basicConfig(filename='/home/pearlwhite85/webapps/django1_2_7/syncscripts/warehouse2webserver/generate_thumbnails.log')

#####################GENERATE THUMBNAILS FUNCTION###########
def generate_and_save_thumbnail(imageFile, h, w, outFile):
    image = Image.open(imageFile)
    image = image.resize((w, h), Image.ANTIALIAS)
    
    image.save(outFile)
	

try:
	# set the image file name here
	myImageFile = sys.argv[1]#full filename with path
	filename=sys.argv[2]#just the filename without path
	outFileLocation = "/home/pearlwhite85/webapps/django1_2_7/ecomstore/static/images/products/thumbnails/"#folder at which thumbnail is to be saved
	outFile=outFileLocation+filename
	# set height
	h = 200
	# set width
	w = 200

	print 'trying to generate thumbnail'
	generate_and_save_thumbnail(myImageFile, h, w,outFile)#function to generate and save thumbnail
	print 'done with the thumbnail'
except:#if something goes wrong
	print 'something went wrong while creating thumbnail for the the file:',sys.argv[2],sys.exc_info()
	logging.error(sys.argv[2]+'####'+str(sys.exc_info()))