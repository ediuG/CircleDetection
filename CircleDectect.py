import numpy as np
import cv2
import cv2.cv as cv

pause = False
cap = cv2.VideoCapture(0)
ret = cap.set(3, 1280)
ret = cap.set(4, 720)

theObject = [0, 0]

def unsharp_mask(img):
	tmp = cv2.GaussianBlur(img, (5, 5), 5)
	cv2.addWeighted(img, 1.5, tmp, -0.5, 0, img)
	return img


def nothing(x):
	pass


def search_for_movement(threshold_image):
	object_detected = False
	temp = threshold_image
	im2, contours, hierarchy = cv2.findContours(temp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	# if contours vector is not empty, we have found some objects
	if contours.size() > 0:
		object_detected = True
	else:
		object_detected = False

	if object_detected:
		# the largest contour is found at the end of the contours vector
		#we will simply assume that the biggest contour is the object we are looking for.
		largestContourVec.push_back(contours.at(contours.size()-1))
		# make a bounding rectangle around the largest contour then find its centroid
		# this will be the object's final estimated position.
		objectBoundingRectangle = cv2.boundingRect(largestContourVec.at(0))
		xpos = objectBoundingRectangle.x+objectBoundingRectangle.width/2
		ypos = objectBoundingRectangle.y+objectBoundingRectangle.height/2

		# update the objects positions by changing the 'theObject' array values
		theObject[0] = xpos
		theObject[1] = ypos

	x = theObject[0]
	y = theObject[1]

cv2.namedWindow("Track bar")
cv2.createTrackbar("Hough resolution", "Track bar", 1, 100, nothing)
cv2.createTrackbar("Canny threshold", "Track bar", 240, 400, nothing)
cv2.createTrackbar("Accumulator threshold", "Track bar", 90, 300, nothing)
cv2.createTrackbar("Min radius", "Track bar", 10, 50, nothing)
cv2.createTrackbar("Max radius", "Track bar", 60, 200, nothing)

while True:
	print cap.get(5)
	# Capture frame-by-frame
	ret, frame = cap.read()

	if ret:
		# get current position of trackbars
		hough_resolution = cv2.getTrackbarPos("Hough resolution", "Track bar")
		canny_threshold = cv2.getTrackbarPos("Canny threshold", "Track bar")
		accumulator_threshold = cv2.getTrackbarPos("Accumulator threshold", "Track bar")
		minRadius = cv2.getTrackbarPos("Min radius", "Track bar")
		maxRadius = cv2.getTrackbarPos("Max radius", "Track bar")

		# Our operations on the frame come here
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray_blur = cv2.GaussianBlur(gray, (9, 9), 4, 4)
		sharp = unsharp_mask(gray_blur)
		# param_1 : Upper threshold for the internal Canny edge detector
		# param_2 : Threshold for center detection.
		circles = cv2.HoughCircles(sharp, cv.CV_HOUGH_GRADIENT, 2.5, 720 / 4,
								   param1=canny_threshold, param2=accumulator_threshold, minRadius=minRadius,
								   maxRadius=maxRadius)

		# pyrmidal_filter = cv2.pyrMeanShiftFiltering(frame, 10, 10)
		# pyr_gray = cv2.cvtColor(pyrmidal_filter, cv2.COLOR_BGR2GRAY)
		# sharp = unsharp_mask(pyr_gray)
		# circles = cv2.HoughCircles(sharp, cv.CV_HOUGH_GRADIENT, 2, 200,
		#                            param1=200, param2=50, minRadius=0, maxRadius=30)
		if circles is not None:
			circles = np.uint16(np.around(circles))

			for i in circles[0, :]:
				# draw the outer circle
				cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
				# draw the center of the circle
				cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)

				# for i in circles[0, :]:
				#     # draw the outer circle
				#     cv2.circle(sharp, (i[0], i[1]), i[2], (0, 255, 0), 2)
				#     # draw the center of the circle
				#     cv2.circle(sharp, (i[0], i[1]), 2, (0, 0, 255), 3)

		# Display the resulting frame
		# cv2.imshow('Gray', gray)
		# cv2.imshow('Blur', gray_blur)
		cv2.imshow('Color', frame)
		# cv2.imshow('Sharp', sharp)

	else:
		continue

	if cv2.waitKey(1) & 0xFF == ord('p'):
		pause = False
		while pause is True:
			if cv2.waitKey(1) & 0xFF == ord('p'):
				break
	elif cv2.waitKey(1) & 0xFF == ord('q'):
		break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
