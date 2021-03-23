import cv2 as cv
import numpy as np

th1 = 437
th2 = 245
thx = 250
thy = 250
#y2 = 700
area = 0
'''
if you want to implement this script in your own drone,
just sum up the cable height from camera (need to convert pixel into mm or meter)
and height sensor (whatever sensor you use)
'''
persegi = (1280, 0, 468, 0)

def empty():
	pass

cap = cv.VideoCapture('Video FP MV.mp4') #load video

kernel = np.ones((5,5),np.uint8) #membuat kernel

while True:

	ret, img = cap.read()
	roi = img[persegi[3]:persegi[2] , persegi[1]:persegi[0]] #membuat roi
	blur = cv.GaussianBlur(roi.copy(),(5,5),0) #blur video
	imgGray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY) #convert menjadi gray
	edges = cv.Canny(imgGray, th1,th2) #canny
	ret,threshold = cv.threshold(edges, thx,thy, cv.ADAPTIVE_THRESH_GAUSSIAN_C) #threshold
	dilate = cv.dilate(edges, kernel, iterations = 1) #melakukan dilate (memperlebar)
	contours, hierarchy = cv.findContours(dilate, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) #mencari contour
	for c in contours:
		area = cv.contourArea(c) #mendapatkan area contour
		if area:
			print(area)
			if area > 3100:
				#drawcontour = cv.drawContours(img, contours, -1, (0,255,0), 2)
				x,y,w,h = cv.boundingRect(c) #bounding rect
				center_of_rect = ((x + x + w)/2, (y + y + h)/2) #mencari titik tengah bounding rect
				cv.circle(img, (int(center_of_rect[0]),int(center_of_rect[1])), 5, (0,255,255),-1) #menggambar dot
				tulisan = f"Cable Height = {abs(center_of_rect[1] - 720)}" #menuliskan kata posisi kabel dan value y dari titik tengah rect
				#print(int(center_of_rect[1])) 
				rect = cv.rectangle(img, (x,y), (x+w,y+h), (0,0,255),2) #menggambar rect
				cv.putText(img, tulisan, (x,y-5), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1) #menaruh tulisan berisi variable tulisan
		else:
			cv.putText(img, "Error, Too Low", (20,50), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
	cv.imshow('ori', img) #menampilkan
	#cv.imshow('roi', dilate)
	
	if cv.waitKey(1) == 27: #bila ditekan esc, close
		break

cap.release()
cv.destroyAllWindows()