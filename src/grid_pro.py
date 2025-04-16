import cv2
import numpy as np
class GRID:
    def __init__(self,dict):
        self.centers = dict['grid_centers']
        self.BOARD_SIZE = dict['BOARD_SIZE']
        self.GRID_SIZE = dict['GRID_SIZE']
        self.grid = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    def detect_piece(self,roi):
        lower_white = np.array([170, 170, 170])  # 白色阈值
        upper_white = np.array([255, 255, 255])
        lower_black = np.array([0, 0, 0])  # 黑色阈值
        upper_black = np.array([70, 70, 70])
        white_mask = cv2.inRange(roi, lower_white, upper_white)
        black_mask = cv2.inRange(roi, lower_black, upper_black)
        #统计像素数量
        white_pixels = cv2.countNonZero(white_mask)
        black_pixels = cv2.countNonZero(black_mask)

    # 判断棋子颜色
        if white_pixels > 100:  # 白棋
            return 1
        elif black_pixels > 100:  # 黑棋
            return -1
        else:  # 空
            return 0
        
    def update_grid(self,frame):
        for i in range(3):
            for j in range(3):
                x, y =self.centers[i][j]
                # 提取格子区域
                roi = frame[y - self.GRID_SIZE // 4:y + self.GRID_SIZE // 4, x - self.GRID_SIZE // 4:x + self.GRID_SIZE // 4]
                # 检测棋子
                piece = self.detect_piece(roi)
                # 如果检测到棋子且之前为空
                if piece != 0 and self.grid[i][j] == 0:
                    self.grid[i][j] = piece
                    print(f"棋子放入：({i}, {j}), 颜色：{'白棋' if piece == 1 else '黑棋'}, 中心坐标：({x}, {y})")
        print(self.grid)
        return self.grid
    def check_grid(self,frame):
        checked_grid = [[
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]]
        for i in range(3):
            for j in range(3):
                x, y =self.centers[i][j]
                # 提取格子区域
                roi = frame[y - self.GRID_SIZE // 4:y + self.GRID_SIZE // 4, x - self.GRID_SIZE // 4:x + self.GRID_SIZE // 4]
                # 检测棋子
                piece = self.detect_piece(roi)
                # 如果检测到棋子且之前为空
                if piece != 0 and checked_grid.grid[i][j] == 0:
                    checked_grid[i][j] = piece
                    
       
        return checked_grid

    def check_winner(self):
        
        """
        检查九宫格映射中是否有胜利者
        :param grid: 3x3 的九宫格映射
        :return: 1（玩家1胜利），-1（玩家2胜利），0（无胜利者）
        """
        # 检查行
        for row in self.grid:  # 遍历每一行
            if row[0] == row[1] == row[2] and row[0] != 0:
                # 返回获胜玩家的值（1 或 -1）
                return row[0]
        # 检查列
        for col in range(3):  # 遍历列索引（0, 1, 2）
            if self.grid[0][col] == self.grid[1][col] == self.grid[2][col] and self.grid[0][col] != 0:
                # 返回获胜玩家的值（1 或 -1）
                return self.grid[0][col]

        # 检查对角线
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] and self.grid[0][0] != 0:
            #print(f"玩家获胜，颜色：{'白棋' if self.grid[0][0] == 1 else '黑棋'}")
            return self.grid[0][0]
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] and self.grid[0][2] != 0:
            #print(f"玩家获胜，颜色：{'白棋' if self.grid[0][2] == 1 else '黑棋'}")
            return self.grid[0][2]

        # 无胜利者
        return 0

    #def get_grid(self):
        #return self.grid

#写一个映射与中心坐标的联动，用字典，用“one,two,......”来给坐标设置id
#重新写一个找棋盘坐标的程序，通过4个角直接计算出格子中心坐标