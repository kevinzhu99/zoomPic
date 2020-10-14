#----------------------------------------------
#--- Author         : Hosein Nayyeri
#----------------------------------------------
from configs.common_config1 import *

detection_method = 'ImageProc'                                      # ImageProc,FCN
  
if detection_method == 'FCN':
import FCNDetectorV3

# image
D.data['cameraname'] = '10.35.30.17'
D.data['cameraip'] = '10.35.30.17' 
rawimagescale = 0.9                                                 # factor to scale the raw input image 0 to 1
livecamviewarea = 2
x1p,y1p,x2p,y2p = 200,10,500,20                                     # rectangle area used to count pans and run detection 

# image rotation parameters
angle = 0

roiwindow = (260,15,200,450)                                        # x,y w,h part of the raw image to be analysed
roiwindow = [int(x*rawimagescale) for x in roiwindow]
lmts = [5,5,5,5]                                                # for visualization, if fullimage True, limits are used to expand the ROI area, crop it and replace it in the raw image and display
perspectTrasf = False
pntsForPrspctveTrnsfrm = [[0,0],[820,20],[0,340],[820,340]]         # used if perspective transform is applied on the image
pntsForPrspctveTrnsfrm = [[int(x[0]*rawimagescale),int(x[1]*rawimagescale)] for x in pntsForPrspctveTrnsfrm]

#count
cntinglnepos = int(100*rawimagescale)     
cntinglineslope = 999                                               # counting line slope 
deviation = int(35*rawimagescale)                                   # the constant that represents the object counting area around counting line(pixel)
xcountlimit = 30                                             # min x distance from previous object in count area to be counted as new, to prevent double counting in contineues counting mode
ycountlimit = 30                                            # min y distance from previous object in count area to be counted as new, to prevent double counting in contineues counting mode

# linestop
D.data['Prevframe'] = np.ones((roiwindow[3],roiwindow[2],3), np.uint8) # to detect if lines stopped
linestopROI = [0,0,roiwindow[2],roiwindow[3]] # x,y,w,h
linestopthresh = (linestopROI[2]*linestopROI[3])/2
LneStpDtctor = shnutils1.shnLineStopDetector(linestoppedbuffersize,linestopthresh,linestopROI)

# input video
CamReader = shnutils1.shnVideoReader(livecamviewarea = livecamviewarea,cameraip = D.data['cameraip'])

# video writer settings to save video
vidlogheight,vidlogwidth = int(roiwindow[3]*0.5),int(roiwindow[2]*0.5)
movielogger = shnutils1.shnVideoLogger(D,videorecduration = videorecduration, videosdirct = videosdirct, vidlogheight = vidlogheight, vidlogwidth= vidlogwidth,FPS = 10, writeinterval = 1.0)

# Detection settings=======================================================================================================
if detection_method == 'ImageProc':
    kernelsze = 3
    filtercolorlower = [(1, 2, 170)]
    filtercolorupper = [(87, 255, 255)]
    erosinIteration = 3
    dilateIteration = 3
    dilateIterationnoise = 3
    naancounter = shnutils1.shnObjectCounterv2('continuous',cntinglnepos,cntinglineslope,deviation)
    boxesarealimit = [20.0*20.0,100.0*100.0]
elif detection_method == 'FCN':
    filtercolorlower = [(1, 2, 170)]
    filtercolorupper = [(87, 255, 255)]
    inpimgshape = [roiwindow[3],roiwindow[2]]                          # for FCN should be devisable by 4
    windowsshapes = [[32,60],[48,40]]                                  # image size used to train the classifier model
    fcndetector = FCNDetectorV3.shnFCNDetectorV3(modelsDir,FCNmodels,inpimgshape,windowsshapes)
    time.sleep(1)
    naancounter = shnutils1.shnObjectCounterv2('continuous',cntinglnepos,cntinglineslope,deviation)
    boxesarealimit = [18.0*18.0,34.0*34.0]
    FCNconfthresh = 0.99
    FCNnmsthreshold = 0.1
    
recordingflagSS = shnutils1.shnSingleShot()                         # single shot used to take ONE snapshot of the image once the pan reaches a specific postion