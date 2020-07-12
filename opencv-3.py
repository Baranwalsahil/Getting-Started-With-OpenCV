##face detection
import cv2


faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
img = cv2.imread("1.jpg")
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
faces = faceCascade.detectMultiScale(imgGray,1.1,3) ##1.1 is scale factor and 4 is the minimum neighbour box should be retain

for (x,y,w,h) in faces:
	cv2.rectangle(img,(x,y),(x+w,y+h),(123,234,0),2)


cv2.imshow("result",img)
cv2.waitKey(0)