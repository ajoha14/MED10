import numpy as np
import cv2

camera = cv2.VideoCapture(0)
qrdec = cv2.QRCodeDetector()

def display(im, bbox):
    if bbox is not None:
        n = len(bbox)
        if n > 0:
            for j in range(n):
                cv2.line(im, tuple(bbox[j][0]), tuple(bbox[ (j+1) % n][0]), (255,0,0), 3)
        # Display results
    cv2.imshow("Results", im)
    cv2.waitKey(10)

try:
    while(True):
        r, im = camera.read()
        data, bbx, rim = qrdec.detectAndDecode(im)
        display(im,bbx)

except KeyboardInterrupt:
    pass