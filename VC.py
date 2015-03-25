import numpy as np
import cv2
import cv2.cv as cv

cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret:
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (15, 15), 2, 2)
        circles = cv2.HoughCircles(gray_blur, cv.CV_HOUGH_GRADIENT, 1.5, 350,
                                   param1=50, param2=10, minRadius=0, maxRadius=0)
        if circles is not None:
            circles = np.uint16(np.around(circles))

            for i in circles[0, :]:
                # draw the outer circle
                cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # draw the center of the circle
                cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)

        # Display the resulting frame
        # cv2.imshow('frame', gray)
        cv2.imshow('color', frame)
        cv2.imshow('blur', gray_blur)
    else:
        continue

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
