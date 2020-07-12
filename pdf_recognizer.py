import cv2
import numpy as np 


width,height = 480,640

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3,frameWidth)
cap.set(4,frameHeight)
cap.set(10,150) ## for adjusting brightness

def preProcessing(img):
	imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
	imgCanny = cv2.Canny(imgBlur,200,200)
	kernel = np.ones((5,5))
	imgDial = cv2.dilate(imgCanny,kernel,iterations=2)
	imgThres = cv2.erode(imgDial,kernel,iterations=1)

	return imgThres

def getContours(img):
	biggest = np.array([])
	maxArea = 0
	contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) ## detetct the outer contours
	for cnt in contours:
		area = cv2.contourArea(cnt)
		#print(area)
		if area > 5000:##giving threshold to images
			peri = cv2.arcLength(cnt,True)
			#print(peri)
			approx = cv2.approxPolyDP(cnt,0.02*peri,True) ## for getting the corner points
			if area > maxArea & len(approx)==4:
				biggest = approx
				maxArea = area
	cv2.drawContours(imgContour,biggest,-1,(255,0,0),20)
	return biggest


def reorder(myPoints):
	myPoints = myPoints.reshape((4,2))
	myPointsN = np.zeros((4,1,2),np.int32)
	add = myPoints.sum(1)

	myPointsN[0] = myPoints[np.argmin(add)]
	myPointsN[3] = myPoints[np.argmax(add)]

	diff = np.diff(myPoints,axis = 1)
	myPointsN[1] = myPoints[np.argmin(diff)]
	myPointsN[2] = myPoints[np.argmax(diff)]

	return myPointsN


def getWarp(img,biggest):
	
	biggest = reorder(biggest)
	pts1 = np.float32(biggest)
	pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
	matrix = cv2.getPerspectiveTransform(pts1,pts2)
	imgOutput = cv2.warpPerspective(img2,matrix,(width,height))
	imgCrop = imgOutput[20:imgOutput.shape[0]-20,20:imgOutput.shape[1]-20]
	imgCrop = cv2.resize(imgCrop,(width,height))
	return imgCrop


while True:
	success , img = cap.read()
	cv2.resize(img,(width,height))
	imgContour = img.copy()
	imgThres = preProcessing(img)
	biggest = getContours(imgThres)
	warpImg = getWarp(img,biggest)
	cv2.imshow("Result",imgContour)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break


cap.release()
cv2.destroyAllWindows()