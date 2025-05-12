import find_ground_test
import cv2
import grid_pro
import time
import logging


# 打开摄像头，参数0表示默认摄像头
cap = cv2.VideoCapture(0)

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
    try:

        dict = find_ground_test.findground(frame)
        
    except Exception as e:
            # 捕获异常并打印错误信息
            print(f"发生错误: {e}")
            # 继续循环
            continue
  
    
        
            
            
            

    # 按 'q' 键退出循环
    if dict != None:
        print(dict)
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        
        break
time.sleep(3)
grid = grid_pro.GRID(dict)
player = -1
while True:
    ret, frame = cap.read()
        # 检查是否成功读取帧
    if not ret:
        print("无法获取帧，退出...")
        break
    try:
        
        grid.update_grid(frame)
        help = grid.help(player)
        print(help)
        time.sleep(1)
        winner = grid.check_winner()
        if grid.check_winner() != 0:
             print(f"玩家获胜，颜色：{'白棋' if winner == 1 else '黑棋'}")
             break
        time.sleep(2)
    except Exception as e:
            # 捕获异常并打印错误信息
            print(f"发生错误: {e}")
            # 继续循环
            continue
    
          
    
# 释放摄像头并关闭所有窗口
cap.release()
cv2.destroyAllWindows()