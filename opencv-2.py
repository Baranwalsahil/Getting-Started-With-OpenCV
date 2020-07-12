import cv2
import numpy as np

path = "5.png"
img = cv2.imread(path)
imgContour = img.copy()

##contour detection
def getContours(img):
	contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) ## detetct the outer contours
	for cnt in contours:
		area = cv2.contourArea(cnt)
		#print(area)
		if area > 500:##giving threshold to images
			cv2.drawContours(imgContour,cnt,-1,(255,0,0),2)
			peri = cv2.arcLength(cnt,True)
			#print(peri)
			approx = cv2.approxPolyDP(cnt,0.02*peri,True) ## for getting the corner points
			print(len(approx)) ##for mentioning the length
			objCor = len(approx)
			x,y,w,h = cv2.boundingRect(approx)
			if objCor == 3:
				objType = "Triangle"
			elif objCor ==4:
				asp = float(w)/h
				if asp>0.95 and asp < 1.05 :
					objType = "Square"
				else:
					objType = "Rectangle"
			else:
				objType = "Quad"
			cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)
			cv2.putText(imgContour,objType,(x+(w//2)-10,y+(h//2)-10),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,255,34),2)




imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)

#cv2.imshow("gray",imgGray)
#cv2.imshow("blur",imgBlur)
#cv2.imshow("original",img) or we can concatenate to show all images
imgCanny = cv2.Canny(imgBlur,70,70)
getContours(imgCanny)
cv2.imshow("canny",imgCanny)
cv2.imshow("contour",imgContour)
cv2.waitKey(0)