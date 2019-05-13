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
    cap = cv2.VideoCapture("C:/Users/Anders S. Johansen/Desktop/test.mp4")

    pathToDetector = "Models/shape_predictor_68_face_landmarks.dat"
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(pathToDetector)
    
    #Plotting iris gradient
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    #Run
    while(cap.isOpened()): #cap.isOpened()
        ret, frame = cap.read()
        cv2.imshow("input", cv2.resize(frame,None, fx=0.2, fy=0.2))
        cv2.waitKey(10)
        #print(frame.shape)
        #frame = cv2.imread("C:/Users/Anders S. Johansen/Desktop/im1.jpg")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector(gray,1)

        for (i,face) in enumerate(rects):
            #Get facial landmark points
            shape = predictor(gray, face)
            shape = shape_to_np(shape) #36-41(left eye), 42-47(right eye)
            l_eye_p = shape[36:42]
            r_eye_p = shape[42:48]
            
            #f2 = frame
            #for p in shape:
            #    cv2.circle(f2, (p[0], p[1]), 2, (255,0,0), 2)
            #cv2.imwrite("C:/Users/Anders S. Johansen/Desktop/im1-1.jpg", f2)
            ax.clear()
            segmentEye(l_eye_p, frame)
    #Cleanup
    cap.release()
    cv2.destroyAllWindows()

def testhr():
    with open("Logs/P1/05_03-09_00_09.csv") as f:
        data = np.array(f.read().splitlines())

    c = hrProcesser()
    hrbuffer = Buffer(size=100)
    gsrbuffer = Buffer(size=100)
    tsbuffer = Buffer(size=100)

    #SETUP LIVE PLOTTER
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    for i in range(1,len(data)):
        #split log data
        log_data = data[i].split(',',3)
        #make buffers
        tsbuffer.add(log_data[0])
        gsrbuffer.add(float(log_data[1]))
        hrbuffer.add(float(log_data[2]))

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
            plt.plot(gsrbuffer.data)
            plt.scatter(l,disppeaks,c='r')
            plt.show()
            plt.pause(0.01)

def makeHrSignal():
    print("lel")

def segmentEye(points, image, min_size=10):
    #Get bounding box
    bb = bounding_box(points)
    width = bb[1][0] - bb[0][0]
    height = bb[1][1] - bb[0][1]
    #Ignore small bounding boxes
    if width < min_size:
        print("eye too small")
        return 0.0
    #Convert image to Greyscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #Create Mask
    mask = np.zeros(image.shape, dtype=np.uint8)
    mask = cv2.fillPoly(mask, [points],(255))
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    #Apply mask
    gray = cv2.bitwise_and(gray, gray, mask=mask)
    #Crop ROI
    roi = gray[bb[0][1]:bb[1][1], bb[0][0]:bb[1][0]]
    #Histogram equalizatoin (improve contrast)
    blob = cv2.equalizeHist(roi)
    #cv2.imwrite("C:/Users/Anders S. Johansen/Desktop/im1-2.jpg", roi)
    #Blur (to remove noise)
    blob = cv2.medianBlur(blob,5)
    blob = cv2.GaussianBlur(blob, (5,5), 0)
    #Adaptive Threshold / gradient edge detection
    blob = cv2.adaptiveThreshold(blob,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,5,1)
    #Remove Eyelid gradient
    eye_mask = mask[bb[0][1]:bb[1][1], bb[0][0]:bb[1][0]]
    blob = cv2.bitwise_and(blob, blob, mask=eye_mask)
    #Hit And Fit
    kernel = np.ones((3,3),np.uint8)
    blob = cv2.erode(blob, kernel, iterations=1)
    #blob = cv2.dilate(blob, kernel, iterations=2)
    #cv2.imwrite("C:/Users/Anders S. Johansen/Desktop/im1-3.jpg", blob)
    #Hough Circles
    circles = cv2.HoughCircles(blob, cv2.HOUGH_GRADIENT, 2, 5, param1=45, param2=20, minRadius=int(width/8), maxRadius=int(width/2))
    #Ignore if no iris detected
    if circles is None:
        print("Couldnt find Iris")
        return 0.0
    circles = np.uint16(np.around(circles))
    best_circle = circles[0,0]
    pupil_ratio(roi, best_circle)
    
    #Iris Location is at the cente
    #Debug
    print("eye found")
    f3 = cv2.equalizeHist(gray[bb[0][1]:bb[1][1], bb[0][0]:bb[1][0]])
    #cv2.imwrite("C:/Users/Anders S. Johansen/Desktop/im1-5.jpg",f3)
    cv2.circle(f3, (best_circle[0],best_circle[1]), 0, (255,0,0), 2)
    cv2.circle(f3, (best_circle[0],best_circle[1]), best_circle[2], (255,0,0), 1)
    #cv2.imwrite("C:/Users/Anders S. Johansen/Desktop/im1-4.jpg",f3)
    cv2.imshow("eye", np.hstack((roi,blob)))
    cv2.waitKey(1)

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

def auto_canny(image, sigma=0.30):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)

	# return the edged image
	return edged

def pupil_ratio(image, pupil_cord):
    gradient_x = image[pupil_cord[1], :]
    gradient_x = np.gradient(gradient_x)
    gradient_x = qm.moving_average(gradient_x, 5)
    peaks = qm.ampd(gradient_x,limit=0.5)

    
    for p in peaks:
        cv2.circle(image, (p,pupil_cord[1]), 0, (255,0,0), 2)
    plt.plot(gradient_x)
    plt.show()
    plt.pause(0.01)

#testEyeTrack()
testhr()