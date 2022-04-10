import cv2
from cv2 import THRESH_BINARY

originalImage = cv2.imread("/Users/jameschen/CS215/Transportation-Tour-Service/cebacity.png")
grayImage = cv2.cvtColor(originalImage,cv2.COLOR_BGR2GRAY)

#(thresh,blackAndWhiteImage)=cv2.threshold(grayImage,127,255,cv2.THRESH_BINARY)
#cv2.imshow('Black white image',blackAndWhiteImage)
cv2.imshow('Original image',originalImage)
cv2.imshow('Gray image',grayImage)
threshold_img = cv2.threshold(grayImage,127,255,cv2.THRESH_BINARY)[1]
cv2.imshow('threshold',threshold_img)
cv2.waitKey(0)
cv2.destroyAllWindows()