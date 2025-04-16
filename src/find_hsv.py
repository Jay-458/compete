import cv2
import numpy as np
def empty(x):
    print(x)
img = cv2.imread("D:\\AK48\\Pictures\\Camera Roll\\WIN_20250326_15_18_14_Pro.jpg")
img = cv2.resize(img,(500,500))
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

#创建一个命名窗口
cv2.namedWindow('trackbar',cv2.WINDOW_AUTOSIZE)
#创建色调滑动条，控制最小色调值
cv2.createTrackbar('hue-min','trackbar',0,180,empty)
#创建色调滑动条，控制最大色调值
cv2.createTrackbar('hue-max','trackbar',180,180,empty)
#创建饱和度滑动条，控制最小值
cv2.createTrackbar('sat-min','trackbar',0,255,empty)
#创建饱和度滑动条，控制最大值
cv2.createTrackbar('sat-max','trackbar',255,255,empty)
#创建亮度滑动条，控制最小亮度
cv2.createTrackbar('val-min','trackbar',0,255,empty)
#创建亮度滑动条，控制最大亮度\
cv2.createTrackbar('val-max','trackbar',255,255,empty)

while True:
    h_min = cv2.getTrackbarPos('hue-min','trackbar')
    h_max = cv2.getTrackbarPos('hue-max','trackbar')
    s_min = cv2.getTrackbarPos('sat-min','trackbar')
    s_max = cv2.getTrackbarPos('sat-max','trackbar')
    val_min = cv2.getTrackbarPos('val-min','trackbar')
    val_max = cv2.getTrackbarPos('val-max','trackbar')
    
    lower = np.array([h_min,s_min,val_min])
    upper = np.array([h_max,s_max,val_max])

    mask = cv2.inRange(hsv,lower,upper)

    result = cv2.bitwise_and(img,img,mask=mask)
    cv2.imshow('mask',mask)
    cv2.imshow('trackbar',result)
    cv2.imshow('img',img)
    cv2.waitKey(1)