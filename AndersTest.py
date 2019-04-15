from Signals.hrProc import hrProcesser
from misc.buffer import Buffer
import misc.QuickMaths as qm
import matplotlib.pyplot as plt
import numpy as np
import imutils, dlib

import cv2
import Signals.eyeSignal as eye

def testEyeTrack():
    #Initialization
    cap = cv2.VideoCapture(0)

    pathToDetector = "Models/shape_predictor_68_face_landmarks.dat"
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(pathToDetector)

    #Run
    while(True):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector(gray,1)

        for (i,rect) in enumerate(rects):
            #Get facial landmark points
            shape = predictor(gray, rect)
            shape = shape_to_np(shape) #36-41(left eye), 42-47(right eye)
            lbb = bounding_box(shape[36:42])
            rbb = bounding_box(shape[42:48])
            #Calculate bounding box width & Height
            l_width = lbb[1][0] - lbb[0][0]
            r_width = rbb[1][0] - rbb[0][0]
            l_height= lbb[1][1] - lbb[0][1]
            r_height= rbb[1][1] - rbb[0][1]
            #Calculate Center
            l_center = (int(lbb[0][0] + l_width/2), int(lbb[0][1] + (l_height/2)))
            r_center = (int(rbb[0][0] + l_width/2), int(rbb[0][1] + (r_height/2)))
            #Cropout eye
            l_eye = frame[l_center[1]-int(l_width/2):l_center[1]+int(l_width/2), l_center[0]-int(l_width/2):l_center[0]+int(l_width/2)]
            r_eye = frame[r_center[1]-int(r_width/2):r_center[1]+int(r_width/2), r_center[0]-int(r_width/2):r_center[0]+int(r_width/2)]
            #grey eye
            l_eye = cv2.cvtColor(l_eye, cv2.COLOR_BGR2GRAY)
            r_eye = cv2.cvtColor(r_eye, cv2.COLOR_BGR2GRAY)
            #Median Filter
            l_eye = cv2.medianBlur(l_eye, 5)
            r_eye = cv2.medianBlur(r_eye, 5)
            #Histogram equalization
            l_eye = cv2.equalizeHist(l_eye)
            r_eye = cv2.equalizeHist(r_eye)
            #Invert
            l_eye = (255 - l_eye)
            r_eye = (255 - r_eye)
            #thresholding
            circles = cv2.HoughCircles(l_eye,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
            
            if circles is not None:
                circles = np.uint16(np.around(circles))
                for i in circles[0,:]:
                    # draw the outer circle
                    cv2.circle(l_eye,(i[0],i[1]),i[2],(0,255,0),1)
                    # draw the center of the circle
                    cv2.circle(l_eye,(i[0],i[1]),2,(0,0,255),2)

            #Show Images
            if l_eye.shape[0] > 0 and l_eye.shape[1] > 0 and r_eye.shape[0] > 0 and r_eye.shape[1]:
                for p in shape[36:42]:
                    cv2.circle(frame, (p[0],p[1]), 1, (0,0,255),1)
                for p in shape[42:48]:
                    cv2.circle(frame, (p[0],p[1]), 1, (0,0,255),1)
                cv2.circle(frame, l_center, 1, (255,0,0),1)
                cv2.circle(frame, r_center, 1, (255,0,0),1)
                cv2.imshow("Image",frame)
                cv2.imshow("left eye", cv2.resize(l_eye, (0,0), fx=4, fy=4))
                cv2.imshow("right eye", cv2.resize(r_eye, (0,0), fx=4, fy=4))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    #Cleanup
    cap.release()
    cv2.destroyAllWindows()

def testhr():
    with open("Logs/03_27-09_04_33.csv") as f:
        data = np.array(f.read().splitlines())

    c = hrProcesser()
    hrbuffer = Buffer(size=100)
    tsbuffer = Buffer(size=100)

    #SETUP LIVE PLOTTER
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    for i in range(1,len(data)):
        hrbuffer.add(float(data[i].split(',',3)[2]))
        tsbuffer.add(data[i].split(',',3)[0])
        if len(hrbuffer.data) == hrbuffer.size:       
            #Do calculations
            hrdat = np.asarray(qm.moving_average(hrbuffer.data,window=10))
            tsdat = np.asarray(tsbuffer.data)
            l = qm.ampd(hrdat,limit=0.5) #Peak Detectoin  
            hrs = c.HR(hrdat,tsdat)
            #plot Data
            disppeaks = []
            for dp in l:
                disppeaks.append(hrdat[int(dp)])
            #Update plot
            ax.clear()
            ax.set_title("HeartRate: {} ({} Samples)".format(hrs,len(disppeaks)))
            plt.plot(hrbuffer.data)
            plt.plot(hrdat)        
            plt.scatter(l,disppeaks,c='r')
            plt.show()
            plt.pause(0.01)

def rect_to_bb(rect):
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y

    # return a tuple of (x, y, w, h)
    return (x, y, w, h)

def shape_to_np(shape, dtype="int"):
    # initialize the list of (x, y)-coordinates
    coords = np.zeros((68, 2), dtype=dtype)

    # loop over the 68 facial landmarks and convert them
    # to a 2-tuple of (x, y)-coordinates
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)

    # return the list of (x, y)-coordinates
    return coords

def bounding_box(points):
    x_coordinates, y_coordinates = zip(*points)
    return [(min(x_coordinates), min(y_coordinates)), (max(x_coordinates), max(y_coordinates))]

def auto_canny(image, sigma=0.99):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
 
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
 
	# return the edged image
	return edged

def iris_segment(image):
    #Using daugmans method

    #Convert image to greyscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    

    return image
    

testEyeTrack()