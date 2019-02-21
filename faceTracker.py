import numpy as np
import cv2 as cv
import argparse



#Functions
def getFeatures(videoCapture):
    ret, frame =  videoCapture.read()
    frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    features = cv.goodFeaturesToTrack(frame,100,0.01,10)
    features = np.int0(features)
    #paint features
    for i in features:
        x,y = i.ravel()
        cv.circle(frame,(x,y),3,255,-1)
    return frame, features

def getface(videoCapture):
    #Get Frame
    print("Get face")

def turnLeft():
    print("turning left")

def turnRight():
    print("turn right")


#Initialization
cap = cv.VideoCapture(0)


#Run
while(True):
    im,f = getFeatures(cap)
    cv.imshow("Capture",im)
    print("updated frame")
    cv.waitKey(0)

#Cleanup
cap.release()
cv.destroyAllWindows()

