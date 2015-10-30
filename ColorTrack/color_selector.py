import numpy as np
import cv2
import cv2.cv as cv

__author__ = 'Guide-ce'

cap = cv2.VideoCapture(1)
cap.set(3, 720)
cap.set(4, 720)


def nothing(x):
	pass

cv2.namedWindow("Hough Circles Track bar")
cv2.createTrackbar(
	"Hough resolution", "Hough Circles Track bar", 1, 100, nothing)
cv2.createTrackbar(
	"Canny threshold", "Hough Circles Track bar", 120, 300, nothing)
cv2.createTrackbar(
	"Accumulator threshold", "Hough Circles Track bar", 110, 200, nothing)
cv2.createTrackbar("Min radius", "Hough Circles Track bar", 5, 50, nothing)
cv2.createTrackbar("Max radius", "Hough Circles Track bar", 60, 200, nothing)

cv2.namedWindow("Track bar")
cv2.createTrackbar("H_MIN", "Track bar", 0, 180, nothing)
cv2.createTrackbar("H_MAX", "Track bar", 180, 180, nothing)
cv2.createTrackbar("S_MIN", "Track bar", 0, 256, nothing)
cv2.createTrackbar("S_MAX", "Track bar", 256, 256, nothing)
cv2.createTrackbar("V_MIN", "Track bar", 0, 256, nothing)
cv2.createTrackbar("V_MAX", "Track bar", 256, 256, nothing)

ball_before = 0

while True:
	hough_resolution = cv2.getTrackbarPos(
		"Hough resolution", "Hough Circles Track bar")
	canny_threshold = cv2.getTrackbarPos(
		"Canny threshold", "Hough Circles Track bar")
	accumulator_threshold = cv2.getTrackbarPos(
		"Accumulator threshold", "Hough Circles Track bar")
	minRadius = cv2.getTrackbarPos("Min radius", "Hough Circles Track bar")
	maxRadius = cv2.getTrackbarPos("Max radius", "Hough Circles Track bar")

	H_MIN = cv2.getTrackbarPos("H_MIN", "Track bar")
	H_MAX = cv2.getTrackbarPos("H_MAX", "Track bar")
	S_MIN = cv2.getTrackbarPos("S_MIN", "Track bar")
	S_MAX = cv2.getTrackbarPos("S_MAX", "Track bar")
	V_MIN = cv2.getTrackbarPos("V_MIN", "Track bar")
	V_MAX = cv2.getTrackbarPos("V_MAX", "Track bar")
	ret, frame = cap.read()

	if ret:
		hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		hsv_range = cv2.inRange(hsv_image, cv.Scalar(H_MIN, S_MIN, V_MIN), cv.Scalar(H_MAX, S_MAX, V_MAX))
		hsv_blur = cv2.GaussianBlur(hsv_range, (9, 9), 4, 4)
		circles = cv2.HoughCircles(hsv_blur, cv.CV_HOUGH_GRADIENT, 2.5, 720 / 4,
								   param1=canny_threshold, param2=accumulator_threshold, minRadius=minRadius,
								   maxRadius=maxRadius)
		ball_count = 0
		if circles is not None:
			circles = np.uint16(np.around(circles))
			for i in circles[0, :]:
				ball_count += 1
				# draw the outer circle
				cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
				# draw the center of the circle
				cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)
		cv2.imshow('color', frame)
		cv2.imshow('hsv', hsv_range)
		# cv2.imshow('hsv', hsv_image)
		print(ball_count)
	else:
		continue
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
