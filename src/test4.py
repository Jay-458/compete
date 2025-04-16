import cv2
import find_blackchess
cap = cv2.VideoCapture(0)
rows_range = slice(0, 720)
cols_range = slice(0, 130)
# 检查摄像头是否成功打开
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

while True:
    
    # 读取一帧视频
    ret, frame = cap.read()
        # 检查是否成功读取帧
    if not ret:
        print("无法获取帧，退出...")
        break
    
    cv2.imshow('frame',frame[rows_range,cols_range])
    if cv2.waitKey(1) & 0xFF == ord('q'):
        
        break

    