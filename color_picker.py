import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3,frameWidth)
cap.set(4,frameHeight)
cap.set(10,150) ## for adjusting brightness


def empty(a):
	pass
cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars",640,240)
cv2.createTrackbar("Hue Min","Trackbars",0,179,empty)
cv2.createTrackbar("Hue Max","Trackbars",179,179,empty)
cv2.createTrackbar("Sat Min","Trackbars",0,255,empty)
cv2.createTrackbar("Sat Max","Trackbars",255,255,empty)
cv2.createTrackbar("Val Min","Trackbars",0,255,empty)
cv2.createTrackbar("Val Max","Trackbars",255,255,empty)


while True:
	sucess , img = cap.read()
	##cv2.imshow("Result",img)
	imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	h_min = cv2.getTrackbarPos("Hue Min","Trackbars")
	h_max = cv2.getTrackbarPos("Hue Max","Trackbars")
	s_min = cv2.getTrackbarPos("Sat Min","Trackbars")
	s_max = cv2.getTrackbarPos("Sat Max","Trackbars")
	v_min = cv2.getTrackbarPos("Val Min","Trackbars")
	v_max = cv2.getTrackbarPos("Val Max","Trackbars")
	##print(h_min,h_max,s_min,s_max,v_min,v_max)
	lower = np.array([h_min,s_min,v_min])
	upper = np.array([h_max,s_max,v_max])
	mask = cv2.inRange(imgHSV,lower,upper)
	##cv2.imshow("HSV",imgHSV)
	##cv2.imshow("mask",mask)## now by adjusting trackbar change its value it createTracker window i.e. black and white
	## but for getting specific image we can get it as follows
	imgResult = cv2.bitwise_and(img,img,mask=mask)
	mask = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
	hStack = np.hstack([img,mask,imgResult])
	cv2.imshow("Result",hStack)
	##cv2.imshow("colored image",imgResult)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()