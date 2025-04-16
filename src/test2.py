import find_ground_pro
import cv2
import grid_test
import time
import AIplayer
import copy
import find_blackchess
import find_whitechess

rows_range = slice(0, 720)
cols_range = slice(0, 130)
# 打开摄像头，参数0表示默认摄像头
cap = cv2.VideoCapture(0)

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

while True:
    ret, frame = cap.read()
        # 检查是否成功读取帧
    
    if not ret:
        print("无法获取帧，退出...")
        break

    try:
            result1 = find_blackchess.findblack(frame[rows_range, cols_range])
            result2 = find_whitechess.findwhite(frame)
            find_ground_pro.findground(frame)
            print(result2)
            print(result1)
    except Exception as e:
                # 捕获异常并打印错误信息
                print(f"发生错误: {e}")
                # 继续循环
                continue
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        
        break
          
    
# 释放摄像头并关闭所有窗口
cap.release()
cv2.destroyAllWindows()