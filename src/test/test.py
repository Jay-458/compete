'''
实验名称：USB摄像头使用
实验平台：核桃派1B
'''

import cv2

cam = cv2.VideoCapture(0) # 打开摄像头，确认好编号

while (cam.isOpened()): # 确认被打开
    
    retval, img = cam.read() # 从摄像头中实时读取图像
    
    cv2.imshow("Video", img) # 在窗口中显示读取到的图像
    
    key = cv2.waitKey(1) # 窗口的图像刷新时间为1毫秒，防止阻塞
    
    if key == 32: # 如果按下空格键，打断
        break
    
cam.release() # 关闭摄像头
cv2.destroyAllWindows() # 销毁显示摄像头视频的窗口
