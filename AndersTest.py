from Signals.hrProc import hrProcesser
from misc.buffer import Buffer
import misc.QuickMaths as qn
import matplotlib.pyplot as plt
import numpy as np

import cv2
import Signals.eyeSignal as eye

def testEyeTrack():
    #Initialization
    cap = cv2.VideoCapture(0)

    #Run
    while(True):
        faceDetector, eyeDetector, detector = eye.init_cv()

        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        im, imGrey, lest, rest, x, y = eye.detect_face(frame, gray, faceDetector)
        leftEye, rightEye, leftEyeG, rightEyeG = eye.detect_eyes(im, imGrey, lest, rest, eyeDetector)
        if leftEye is not None:
            leftEyeKP = eye.process_eye(leftEye,200,detector)
            eye.draw_blobs(leftEye, leftEyeKP)
            print(leftEyeKP)
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
            hrs = c.heartRate(hrdat,tsdat)
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

testEyeTrack()