import numpy as np
import cv2
import cv2.cv as cv

cap = cv2.VideoCapture(0)

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret:
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (9, 9), 0)
        # circles = cv2.HoughCircles(blur, cv.CV_HOUGH_GRADIENT, 1, 20,
        #                            param1=50, param2=30, minRadius=0, maxRadius=0)

        #Draw circle in frame
        cv2.circle(gray, (100, 100), 20, (0, 255, 255),4)

        # Display the resulting frame
        cv2.imshow('frame', gray)
        cv2.imshow('blur', blur)
    else:
        continue

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
