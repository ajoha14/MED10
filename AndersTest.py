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
    cap = cv2.VideoCapture("C:/Users/Anders S. Johansen/Desktop/im/vid.mp4")

    pathToDetector = "Models/shape_predictor_68_face_landmarks.dat"
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(pathToDetector)

    #Run
    while(cap.isOpened()):
        ret, frame = cap.read()
        #frame = cv2.imread("C:/Users/Anders S. Johansen/Desktop/im/5.jpg")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector(gray,1)

        for (i,rect) in enumerate(rects):
            #Get facial landmark points
            shape = predictor(gray, rect)
            shape = shape_to_np(shape) #36-41(left eye), 42-47(right eye)
            l_eye_p = shape[36:42]
            r_eye_p = shape[42:48]
            lbb = bounding_box(l_eye_p)
            rbb = bounding_box(r_eye_p)
            #Calculate bounding box width & Height
            l_width = lbb[1][0] - lbb[0][0]
            r_width = rbb[1][0] - rbb[0][0]
            l_height= lbb[1][1] - lbb[0][1]
            r_height= rbb[1][1] - rbb[0][1]
            #Calculate Center
            l_center = (int(lbb[0][0] + l_width/2), int(lbb[0][1] + (l_height/2)))
            r_center = (int(rbb[0][0] + l_width/2), int(rbb[0][1] + (r_height/2)))
            #Cropout eye
            l_eye = gray[l_center[1]-int(l_width/2):l_center[1]+int(l_width/2), l_center[0]-int(l_width/2):l_center[0]+int(l_width/2)]
            r_eye = gray[r_center[1]-int(r_width/2):r_center[1]+int(r_width/2), r_center[0]-int(r_width/2):r_center[0]+int(r_width/2)]
            #Create Mask
            im_mask = np.zeros(frame.shape, dtype=np.uint8)
            im_mask = cv2.fillPoly(im_mask, [l_eye_p],(255,255,255))
            im_mask = cv2.fillPoly(im_mask, [r_eye_p],(255,255,255))
            im_mask = cv2.cvtColor(im_mask, cv2.COLOR_BGR2GRAY)
            l_mask = im_mask[l_center[1]-int(l_width/2):l_center[1]+int(l_width/2), l_center[0]-int(l_width/2):l_center[0]+int(l_width/2)]
            r_mask = im_mask[r_center[1]-int(r_width/2):r_center[1]+int(r_width/2), r_center[0]-int(r_width/2):r_center[0]+int(r_width/2)]
            #Apply Mask
            left_eye = frame[l_center[1]-int(l_width/2):l_center[1]+int(l_width/2), l_center[0]-int(l_width/2):l_center[0]+int(l_width/2)]
            right_eye = frame[r_center[1]-int(r_width/2):r_center[1]+int(r_width/2), r_center[0]-int(r_width/2):r_center[0]+int(r_width/2)]
            left_eye = cv2.bitwise_and(left_eye, left_eye, mask=l_mask)
            right_eye = cv2.bitwise_and(right_eye, right_eye, mask=r_mask)

        #Show Images
        cv2.circle(frame, l_center, 1, (255,0,0),1)
        cv2.circle(frame, r_center, 1, (255,0,0),1)
        cv2.imshow("Image",frame)
        cv2.imshow("left eye", left_eye)
        cv2.imshow("left mask", right_eye)
        cv2.waitKey(1)
        if 0xFF == ord('q'):
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