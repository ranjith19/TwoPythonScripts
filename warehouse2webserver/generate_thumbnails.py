import Image
import sys
import logging
logging.basicConfig(filename='/home/pearlwhite85/webapps/django1_2_7/syncscripts/warehouse2webserver/generate_thumbnails.log')


def generate_and_save_thumbnail(imageFile, h, w, outFile):
    image = Image.open(imageFile)
    image = image.resize((w, h), Image.ANTIALIAS)
    
    image.save(outFile)
try:
	# set the image file name here
	myImageFile = sys.argv[1]
	filename=sys.argv[2]
	outFileLocation = "/home/pearlwhite85/webapps/django1_2_7/ecomstore/static/images/products/thumbnails/"
	outFile=outFileLocation+filename
	# set height
	h = 200
	# set width
	w = 200

	print 'trying to generate thumbnail'
	generate_and_save_thumbnail(myImageFile, h, w,outFile)
	print 'done with the thumbnail'
except:
	print 'something went wrong while creating thumbnail for the the file:',sys.argv[2],sys.exc_info()
	logging.error(sys.argv[2]+'####'+str(sys.exc_info()))