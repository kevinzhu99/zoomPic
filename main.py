from flask import Flask
from flask import render_template, url_for, request, redirect
import os
from PIL import Image
import time


#functions:
from functions import *


app = Flask(__name__)

APP_ROUTE = os.path.dirname(os.path.abspath(__file__))							#getting the image path


@app.route('/', methods = ['GET', 'POST'])
def index():
	
	imageCam, imageArea , imgRotAng, imgRotRoi_window, imgRotPerspect, imgPntsTransform, countNum,  \
		detectBoxLim, detectFCNThresh, detectFCNthreshold = getValue()

	

	return render_template('index.html', imageCam = imageCam, imageArea = imageArea, imgRotAng = imgRotAng, imgRotRoi_window = imgRotRoi_window, imgRotPerspect = imgRotPerspect \
		,imgPntsTransform = imgPntsTransform, countNum = countNum, detectBoxLim = detectBoxLim, detectFCNThresh = detectFCNThresh , detectFCNthreshold = detectFCNthreshold)



@app.route('/shnGetCamImg', methods = ['GET', 'POST'])
def shnGetCamImg():
	

	editKeyVal = {}
	if request.method == 'POST':
		cameraip = request.form['cameraIP']
		

		#create a dictionary, update it here - pass one dictionary, assign all the
		editKeyVal["D.data['cameraname']"] = request.form['cameraIP']
		editKeyVal["D.data['cameraip']"] = editKeyVal["D.data['cameraname']"]
		editKeyVal['livecamviewarea'] = request.form['imageArea']
		editKeyVal['angle'] = request.form['imgRotAng']
		editKeyVal['roiwindow'] = request.form['imgRotRoi_window']
		editKeyVal['perspectTrasf'] = request.form['imgRotPerspect']
		editKeyVal['pntsForPrspctveTrnsfrm']= request.form['imgPntsTransform']
		editKeyVal['cntinglnepos'] = request.form['countNum']
		editKeyVal['boxesarealimit'] = request.form['detectBoxLim']
		editKeyVal['FCNconfthresh']= request.form['detectFCNThresh']
		editKeyVal['FCNnmsthreshold'] = request.form['detectFCNthreshold']	

		#this is for the cropped image
		start_X = int(request.form['startX_Coord'])
		start_Y = int(request.form['startY_Coord'])
		
		width_XY = int(request.form['width_Coord'])
		height_XY = int(request.form['height_Coord'])

		#this is for the image points transform
		pnt1 = (request.form['pnt1Transform'])
		pnt2 = (request.form['pnt2Transform'])
		pnt3 = (request.form['pnt3Transform'])
		pnt4 = (request.form['pnt4Transform'])

		#we want to see what photo we actually want
		pic_type = (request.form['picOptions'])
		



	test = setValue(editKeyVal)
	
	imgtest, imgCrop, transformed_image, final_image = imageProcessing(cameraip, start_X, start_Y, width_XY, height_XY, pnt1, pnt2, pnt3, pnt4)

	imgtest, imgCrop, transformed_image, final_image = updateFolder(cameraip, imgtest, imgCrop, transformed_image, final_image)

	if pic_type == "Original Image":
		picType_photo = imgtest
	elif pic_type == "Cropped Image":
		picType_photo = imgCrop
	elif pic_type == "Transformed Image":
		picType_photo = transformed_image
	else:
		picType_photo = final_image


	return render_template('display.html', imgtest=imgtest, imgCrop = imgCrop, cIP=editKeyVal["D.data['cameraname']"], iArea = editKeyVal['livecamviewarea'], cAng = editKeyVal['angle'], cROI = editKeyVal['roiwindow'], cPer = editKeyVal['perspectTrasf'], \
		iPnts = editKeyVal['pntsForPrspctveTrnsfrm'], cCnt = editKeyVal['cntinglnepos'], cBox = editKeyVal['boxesarealimit'], cFCN = editKeyVal['FCNconfthresh'], ctHold = editKeyVal['FCNnmsthreshold'],\
		start_X = start_X, start_Y=start_Y, width_XY = width_XY, height_XY = height_XY, pnt1=pnt1,pnt2=pnt2,pnt3=pnt3,pnt4=pnt4, pic_type = pic_type, picType_photo = picType_photo )


#*********************************************************************************************************************************************************************************#

@app.route("/picture")
def picture():
	return render_template("upload.html")

@app.route("/upload", methods = ['POST'])
def upload():
	target = os.path.join(APP_ROUTE, 'static/')									#uploading into a directory called static
	print(target)


	if not os.path.isdir(target):
		os.mkdir(target)

	else:
		print("Couldn't create the directory: {}" .format(target))
	print(request.files.getlist("file"))


	for file in request.files.getlist("file"):
		print(file)
		filename = file.filename
		destination = "/".join([target, filename])
		print(destination)
		file.save(destination)
		picImage = Image.open(destination)
		width, height = picImage.size


	return render_template("complete.html", image_name = filename, width=width, height=height)

#@app.route("/editImage")
#def editImage():

	

@app.route("/gallery")
def get_gallery():
	image_names = os.listdir('./static')
	print(image_names)
	return render_template("gallery.html", image_names = image_names)

if __name__ == '__main__':
	app.run()           