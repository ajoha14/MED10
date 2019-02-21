import numpy as np
import cv2

#Functions
def findFace(videoCapture):
    # Capture frame-by-frame
    ret, frame = videoCapture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1, minSize=(1,1))
    
    # Draw a rectangle around the faces
    face = [0,0,0,0]
    for f in faces:
        if face[2]*face[3] < f[2]*f[3]:
            face = f
    
    # Display the resulting frame
    return frame, face

def turn(turnFactor):
    print("Turning: " + str(turnFactor))


#Initialization
cap = cv2.VideoCapture(0)
faceCascade = cv2.CascadeClassifier("c:/Users/Anders S. Johansen/Documents/MED10/facedetection/faceDetectWeights.xml")

#Run
while(True):
    frame,face = findFace(cap)
    xOffset = 0
    if face[2]*face[3] > 20000: #Face size threshold
        cv2.rectangle(frame, (face[0], face[1]), (face[0]+face[2], face[1]+face[3]), (0, 255, 0), 2)
        xOffset = int(frame.shape[1]/2) - int(face[0]+(face[3]/2))
        cv2.line(frame, (int(frame.shape[1]/2),100), (int(frame.shape[1]/2)+xOffset,100),(255,0,0),5)
        cv2.imshow("Face",frame)
    turn(xOffset)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Cleanup
cap.release()
cv2.destroyAllWindows()
