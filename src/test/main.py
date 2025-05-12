import find_blackchess
import grid_pro
import transfer
import cv2
import time
import find_whitechess
import find_ground_pro
import send


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

                


def main():
    mode = input("请输入模式(A/B)：")
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
    grid = grid_pro.GRID(dict)
    print("初始化棋盘完成")

    if mode == "A":
        
        while True:
            ret,frame = cap.read()
            blackchess_list = find_blackchess.findblack(frame)
            if len(blackchess_list) != 0 :
                break
            
        point1 = transfer.convert_coordinate(blackchess_list[-1])
        point2 = transfer.convert_coordinate(centers[1][1])
        sender.send_packed_data(point1,point2)
        print("已发送")
    if mode == "A":
        
        while True:
            ret,frame = cap.read()
            blackchess_list = find_blackchess.findblack(frame)
            if len(blackchess_list) != 0 :
                break
            
        point1 = transfer.convert_coordinate(blackchess_list[-1])
        point2 = transfer.convert_coordinate(centers[1][1])
        sender.send_packed_data(point1,point2)
        print("已发送")
 

    elif mode == "B":
        rows_range = slice(0, 720)
        cols_range = slice(0, 130)
        while True:
            place = int(input("想要放入的位置："))
            color = int(input("请输入棋子颜色（黑棋为-1，白棋为1）:"))
            while True:
                ret,frame = cap.read()
                blackchess_list = find_blackchess.findblack(frame)
                whitechess_list = find_whitechess.findwhite(frame[rows_range,cols_range])
                if color == -1 and len(blackchess_list) != 0 :
                        print(blackchess_list)
                        print("棋子已识别，请勿再移动棋子")
                        break
                elif color == 1 and len(whitechess_list) != 0:
                        print(whitechess_list)
                        print("棋子已识别，请勿再移动棋子")
                        break
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            if color == -1:
                point1 = transfer.convert_coordinate(blackchess_list[-1])
            elif color == 1:
                point1 =  transfer.convert_coordinate(whitechess_list[-1]) 
            point2 = transfer.convert_coordinate(place_to_point(place,centers))
            print(point1,point2)
            time.sleep(3)
            sender.send_packed_data(point1,point2)
            print("已发送")  
    # 释放摄像头并关闭所有窗口
    #cap.release()
    #cv2.destroyAllWindows()

if __name__ == "__main__":
    

    sender = send.Sender('COM10', 9600)
    main()