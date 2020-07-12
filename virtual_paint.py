import cv2
import numpy as np 

frameWidth = 1040
frameHeight = 840
cap = cv2.VideoCapture(0)
cap.set(3,frameWidth)
cap.set(4,frameHeight)
cap.set(10,150) ## for adjusting brightness

myColors = [[107,89,0,152,255,255]]

myColorValues = [[51,153,255]]  ### in the format of BGR

myPoints = [] ## x,y,colorID

def findColor(img,myColors,myColorValues):
	imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	cnt =0
	newPoints = []
	for color in myColors:
		lower = np.array(color[0:3])
		upper = np.array(color[3:6])
		mask = cv2.inRange(imgHSV,lower,upper)
		x,y = getContours(mask)
		cv2.circle(imgResult,(x,y),10,myColorValues[cnt],(cv2.FILLED))
		if x!=0 and y!=0:
			newPoints.append([x,y,cnt])
		cnt += 1
	return newPoints
		#cv2.imshow(str(color[0]),mask)

def getContours(img):
	contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) ## detetct the outer contours
	x,y,w,h = 0,0,0,0
	for cnt in contours:
		area = cv2.contourArea(cnt)
		#print(area)
		if area > 500:##giving threshold to images
			##cv2.drawContours(imgResult,cnt,-1,(255,0,0),2)
			peri = cv2.arcLength(cnt,True)
			#print(peri)
			approx = cv2.approxPolyDP(cnt,0.02*peri,True) ## for getting the corner points
			x,y,w,h = cv2.boundingRect(approx)
	return x+w//2,y

def draw(myPoints,myColorValues):
	for pnt in myPoints:
		cv2.circle(imgResult,(pnt[0],pnt[1]),10,myColorValues[pnt[2]],cv2.FILLED)

while True:
	sucess , img = cap.read()
	imgResult = img.copy()
	newPoints = findColor(img,myColors,myColorValues)
	if len(newPoints) != 0:
		for new in newPoints:
			myPoints.append(new)
	if len(myPoints) != 0:
		draw(myPoints,myColorValues)
	cv2.imshow("Result",imgResult)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break