import numpy as np
import cv2

img = cv2.imread("1.jpg")
kernel = np.ones((5,5),np.uint8)
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray,(7,7),0)

##edge detection
imgCanny = cv2.Canny(img,200,150) ##100 is threshold value te reduce the no. of edge detection
imgDilation = cv2.dilate(imgCanny,kernel,iterations=1)##adding thickness of edge
 
##opposite of dilation
imgEroded  =cv2.erode(imgDilation,kernel,iterations=1)

##cv2.imshow("gray image",imgGray)
##cv2.imshow("blur image",imgBlur)
##cv2.imshow("Canny image",imgCanny)
##cv2.imshow("dilated image",imgDilation)
##cv2.imshow("Eroded image",imgEroded)

##print(img.shape)
imgResize = cv2.resize(img,(300,200))## first width then height
##cv2.imshow("resize image",imgResize)

imgCropped = img[0:700,200:500]
##c2.imshow("cropped image",imgCropped)

img1 = np.zeros((512,512,3),np.uint8)
##img1[200:300,100:300] = 255,0,0 ##img1[:] for whole image
##cv2.imshow("Image",img1)
cv2.line(img1,(0,0),(300,300),(0,255,0),3)
cv2.rectangle(img1,(0,0),(250,350),(255,0,0),3)## for filling it with color instead of thickness provide cv2.FILLED
cv2.circle(img1,(400,50),30,(255,34,35),2)
cv2.putText(img1,"OPENCV",(300,100),cv2.FONT_HERSHEY_COMPLEX,1,(150,0,0),3)
##cv2.imshow("Image",img1)


##warping perspective
img2 = cv2.imread("1.jpg")
width , height = 250,350
pts1 = np.float32([[111,219],[287,188],[154,482],[352,440]])
pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
matrix = cv2.getPerspectiveTransform(pts1,pts2)
imgOutput = cv2.warpPerspective(img2,matrix,(width,height))
##cv2.imshow("card",imgOutput)

img3 = cv2.imread("2.jpg")
imgHor = np.hstack((img3,img3)) ## same for vertical np.vstack
##cv2.imshow("image",imgHor)

##color detection
##trackbar
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
	img = cv2.imread("2.jpg")
	imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	##cv2.imshow("img1",img)
	h_min = cv2.getTrackbarPos("Hue Min","Trackbars")
	h_max = cv2.getTrackbarPos("Hue Max","Trackbars")
	s_min = cv2.getTrackbarPos("Sat Min","Trackbars")
	s_max = cv2.getTrackbarPos("Sat Max","Trackbars")
	v_min = cv2.getTrackbarPos("Val Min","Trackbars")
	v_max = cv2.getTrackbarPos("Val Max","Trackbars")
	print(h_min,h_max,s_min,s_max,v_min,v_max)
	lower = np.array([h_min,s_min,v_min])
	upper = np.array([h_max,s_max,v_max])
	##print(lower)
	mask = cv2.inRange(imgHSV,lower,upper)
	cv2.imshow("HSV",imgHSV)
	cv2.imshow("mask",mask)## now by adjusting trackbar change its value it createTracker window i.e. black and white
	## but for getting specific image we can get it as follows
	imgResult = cv2.bitwise_and(img,img,mask=mask)
	##cv2.imshow("colored image",imgResult)
	cv2.waitKey(1)