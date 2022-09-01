import cv2
from object_detector import *
import numpy as np

#load Aruco detector
parameters = cv2.aruco.DetectorParameters_create()
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)

#obj detecting
detector = HomogeneousBgDetector()

#load image
img = cv2.imread("phone_aruco_marker.jpg")

corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)

#draw polygon around marker
int_corners = np.int0(corners)
cv2.polylines(img, int_corners, True, (0, 255, 0), 5)

#aruco perimeter
aruco_perimeter = cv2.arcLength(corners[0], True)

#pixel to cm ratio
pixel_cm_ratio = aruco_perimeter / 20
print(pixel_cm_ratio)
counters = detector.detect_objects(img)

#drawing the obj boundaries
for ct in counters:
	

	#making into rectangle
	rectangle = cv2.minAreaRect(ct)
	(x, y), (w, h), angle = rectangle

	#converting width and height of obj by applying ratio pixel to cm
	object_width = w / pixel_cm_ratio
	object_height = h / pixel_cm_ratio

	#displaying
	box = cv2.boxPoints(rectangle)
	box = np.int0(box)

	cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
	cv2.polylines(img, [box], True, (255, 0, 0), 2)
	cv2.putText(img, "Width {} cm".format(round(object_width, 4)), (int(x - 50), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
	cv2.putText(img, "Length {} cm".format(round(object_height, 4)), (int(x - 50), int(y + 20)), cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)

cv2.imshow("Image",img)
cv2.waitKey(0)