import find_ground_pro
import find_chess
import AIplayer
import grid_pro
import transfer
import send

import cv2
import numpy as np
import time
import copy
import threading

black_chesses = []
white_chesses = []
centers = []
help = (1,1)
player = -1
mode_grid = []

def place_to_point(place,centers):
    if place == 1:
        return centers[0][0]
    elif place == 2:
        return centers[1][0]
    elif place == 3:
        return centers[2][0]
    elif place == 4:
        return centers[0][1]
    elif place == 5:
        return centers[1][1]
    elif place == 6:
        return centers[2][1]
    elif place == 7:
        return centers[2][0]
    elif place == 8:
        return centers[2][1]
    elif place == 9:
        return centers[2][2]
    else :
        return None
    
def loop():
    # port = 'COM10'
    baudrate = 9600
    # sender = send.Sender(port,baudrate)
    while True:
        mode = input("请输入模式(A/B/C)：")
        if mode == 'A':
            point1 = transfer.convert_coordinate(black_chesses[0])
            point2 = transfer.convert_coordinate(centers[1][1])
            # sender.send_packed_data(point1,point2)
            print("已发送")

        elif mode == 'B':
            while True:
                place = int(input("想要放入的位置："))
                color = int(input("请输入棋子颜色（黑棋为-1，白棋为1）:"))
                if color == -1:
                    try:
                        point1 = transfer.convert_coordinate(black_chesses[0])
                        point2 = transfer.convert_coordinate(place_to_point(place,centers))
                        # sender.send_packed_data(point1,point2)
                        print("已发送")
                    except Exception as e:
                        # 捕获异常并打印错误信息
                        print(f"未找到该颜色的棋子")
                        # 继续循环
                        continue
                elif color == 1:
                    try:
                        point1 = transfer.convert_coordinate(white_chesses[0])
                        point2 = transfer.convert_coordinate(place_to_point(place,centers))
                    except Exception as e:
                        # 捕获异常并打印错误信息
                        print(f"未找到该颜色的棋子")
                        # 继续循环
                        continue
                elif color == 0:
                    break

        elif mode == 'C':
            global player
            player = int(input("请输入棋子颜色（黑棋为-1，白棋为1）:"))
            while True:
                if input("玩家下完请按'Y'") == 'Y':
                    help = AIplayer.help(mode_grid,player)
                    print(help)
                    if player == -1:
                        try:
                            point1 = transfer.convert_coordinate(black_chesses[0])
                            point2 = transfer.convert_coordinate(centers[help[0],help[1]])
                            # sender.send_packed_data(point1,point2)
                            print("已发送")
                        except Exception as e:
                            # 捕获异常并打印错误信息
                            print(f"未找到该颜色的棋子")
                            # 继续循环
                            continue
                       
                        
                    elif player == 1:
                        try:
                            point1 = transfer.convert_coordinate(white_chesses[0])
                            point2 = transfer.convert_coordinate(centers[help[0],help[1]])
                            #sender.send_packed_data(point1,point2)
                            print("已发送")
                        except Exception as e:
                            # 捕获异常并打印错误信息
                            print(f"未找到该颜色的棋子")
                            # 继续循环
                            continue

                    elif color == 0:
                        break
                        

               
def detector():
    cap = cv2.VideoCapture(0)
    global centers,black_chesses,white_chesses,help,mode_grid
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

            dict = find_ground_pro.findground(frame)
            
        except Exception as e:
                # 捕获异常并打印错误信息
                print(f"发生错误: {e}")
                # 继续循环
                continue
    
        if dict != None:
            #print(dict)
            print("已识别到棋盘,请勿再移动棋盘")
            break
        # 按 'q' 键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            
            break

        # 释放摄像头并关闭所有窗口
        cap.release()
        cv2.destroyAllWindows()
    centers = dict['grid_centers']
    print("初始化棋盘完成")
    grid = grid_pro.GRID(dict)
    while True:
        # 读取一帧视频
        ret, frame = cap.read()
        # 检查是否成功读取帧
        if not ret:
            print("无法获取帧，退出...")
            break
        try:
            # 识别棋子
            black_chesses = find_chess.findblack(frame)
            white_chesses = find_chess.findwhite(frame)
            find_chess.draw_chessboard(frame,black_chesses,white_chesses)
            #print(black_chesses)
            cv2.imshow("frame",frame)
            grid.update_grid(frame)
            mode_grid = copy.copy(grid.grid)
            # help = AIplayer.help(mode_grid,player)
            #print(grid.grid)
            # print(help)
            if cv2.waitKey(1) & 0xFF == ord('q'):
            # 释放摄像头并关闭所有窗口
                cap.release()
                cv2.destroyAllWindows()
        except Exception as e:
                # 捕获异常并打印错误信息
                print(f"发生错误: {e}")
                # 继续循环
                continue

t1 = threading.Thread(target= detector)
t2 = threading.Thread(target= loop)
t1.start()
t2.start()

t1.join()
t2.join()