from opencv import cv2
import os
from PIL import Image
import cv2
import time


#this will go in the function for @index
def loadIndex():	
	
	#open the file and make it to write
	with open('testCameraconfig.py', 'r+') as f:
		lines = f.readlines()
		lines = [l for l in lines if '#' not in l]
        
	return lines
	

#this function assigns the dictionary and sets everything up
def setDictionary():
    
    lines = loadIndex()

    keyvallines = [l for l in lines if ('=' in l and '==' not in l)]

    keyvaldic = {}
    
    #setting the dictionary
    for line in  keyvallines:
        equal = line.find('=')
        key = line[0:equal].strip(' ')
        val = line[equal+2:].strip(' ').strip('\n')
        keyvaldic[key] = val
    
    return keyvaldic
    
#this function will inherit getVariable and find the  keys wanted in the dictionary
def getValue():
    
    keyDict = setDictionary()
    
    #image
    imageCam = keyDict["D.data['cameraname']"]                    #answer: '10.35.30.17'
    imageIP = imageCam                       					  #answer: '10.35.30.17' 
    imageArea = keyDict['livecamviewarea']                        #answer: 2
    
    #image rotation parameters
    imgRotAng = keyDict['angle']
    #this is not working
        #coordXY = keyDict['x1p,y1p,x2p,y2p']                            #answer: coordXY isn't showing up 
    
    imgRotRoi_window = keyDict['roiwindow']                               #answer: (260,15,200,450)  or [int(x*rawimagescale) for x in roiwindow]
    
    imgRotPerspect = keyDict['perspectTrasf']                         #answer: False
    
    imgPntsTransform = keyDict['pntsForPrspctveTrnsfrm']               #does not give you the correct output, variable assigned twice
    
    #count
    countNum = keyDict['cntinglnepos']                              #answer: int(100*rawimagescale)
    
    #countDev = keyDict['deviation']                                #answer is not showing up
        
    #countX = keyDict['xcountlimit']                                 #answer does not show
    
    #countY = keyDict['ycountlimit']                                #answer does not show
    
    #Dectection Settings
    detectBoxLim = keyDict['boxesarealimit']                       #answer [20.0*20.0,100.0*100.0]
    
    detectFCNThresh = keyDict['FCNconfthresh']                      #answer 0.99
    
    detectFCNthreshold = keyDict['FCNnmsthreshold']                 #answer 0.1
    
    return imageCam, imageArea , imgRotAng, imgRotRoi_window, imgRotPerspect, imgPntsTransform, countNum,  \
        detectBoxLim, detectFCNThresh, detectFCNthreshold

#imageCam, imageIP ,

def setValue(editKeyVal):
	
	#regenerate the file/ update the file
	with open("testCameraconfig.py", "r") as rf:
		lines = rf.readlines()
		
	
	
	#for key in dictionary key	
	for key in editKeyVal:	
		# #read the line; for line in lines
		for i,line in enumerate(lines):
			line_length = (len(line) - len(line.lstrip()))
			equal = line.find('=')
			if (key in line) and (key in line[0:equal].strip(' ')): #this is incomplete, still not searching properly - add something along the line where you try to find if the key is before the "=" sign
				spaces = line_length*" "
				lines[i] = ("{}{} = {}\n".format(spaces,key,editKeyVal[key]))

				
				

	#open a new file and write over it
	with open("testCameraconfig.txt", "w") as wf:
		for line in lines:
			wf.write(line)



#this will go in the function for @shnGetCamImg
def imageProcessing(cameraip, start_X, start_Y, width_XY, height_XY, pnt1, pnt2, pnt3, pnt4):
	
	livecamviewarea = 2
	
	cap = cv2.VideoCapture('rtsp://root:pass@'+cameraip+'/axis-media/media.amp?&camera=' + str(livecamviewarea))
	ret, frame = cap.read()
	
	
	
	cropPic = frame[start_Y:start_Y+height_XY, start_X:start_X+width_XY]

	# points perspective
	transformed_image = cropPic.copy()

	#final image
	final_image = cropPic.copy()


	#show image
	debug = False	
	if debug:
		cv2.imshow('img',frame)
		cv2.waitKey(0)
	
	cap.release()
	return frame, cropPic, transformed_image, final_image


	
def updateFolder(cameraip,frame, cropPic, transformed_image, final_image):

	#read the image name
	imgtest = "{}.png".format(cameraip + "." + str(time.time()))
	# read the cropped image we create
	imgCrop = "{}.png".format("CROP"+"."+cameraip+"."+str(time.time()))

	imgTransform = "{}.png".format("TRANSFORMED"+"."+cameraip+"."+str(time.time()))

	imgFinal = "{}.png".format("FINAL"+"."+cameraip+"."+str(time.time()))

		# #test to get the list
	list_Files = os.listdir('./static')


	#iterate through the list of files to find the exact one
	for file in list_Files:
		if file.split(".")[0:4] == imgtest.split(".")[0:4]:
			locFile = r'C:/Users/kzhu/Desktop/zoomPic/static'
			path = os.path.join(locFile, file)
			list_Files.remove(file)
			os.remove(path)

	#for image crop
	for file in list_Files:
		if file.split(".")[0:5] == imgCrop.split(".")[0:5]:
			locPath = r"C:/Users/kzhu/Desktop/zoomPic/static" 
			jPath = os.path.join(locPath, file)
			list_Files.remove(file)
			os.remove(jPath)

	#for the transformed image
	for file in list_Files:
		if file.split(".")[0:5] == imgTransform.split(".")[0:5]:
			locPath = r"C:/Users/kzhu/Desktop/zoomPic/static" 
			jPath = os.path.join(locPath, file)
			list_Files.remove(file)
			os.remove(jPath)


	#for the final image		
	for file in list_Files:
		if file.split(".")[0:5] == imgFinal.split(".")[0:5]:
			locPath = r"C:/Users/kzhu/Desktop/zoomPic/static" 
			jPath = os.path.join(locPath, file)
			list_Files.remove(file)
			os.remove(jPath)


	#write out the path for where we will store these images
	cv2.imwrite(r'C:/Users/kzhu/Desktop/zoomPic/static/{}'.format(imgtest),frame)
	cv2.imwrite(r'C:/Users/kzhu/Desktop/zoomPic/static/{}'.format(imgCrop),cropPic)
	cv2.imwrite(r'C:/Users/kzhu/Desktop/zoomPic/static/{}'.format(imgTransform),transformed_image)
	cv2.imwrite(r'C:/Users/kzhu/Desktop/zoomPic/static/{}'.format(imgFinal),final_image)

	return imgtest,imgCrop, imgTransform, imgFinal


