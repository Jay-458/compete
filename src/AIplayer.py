import time
def check_winner(dict):
        
        """
        检查九宫格映射中是否有胜利者
        :param grid: 3x3 的九宫格映射
        :return: 1（玩家1胜利），-1（玩家2胜利），0（无胜利者）
        """
        # 检查行
        for row in dict:  # 遍历每一行
            if row[0] == row[1] == row[2] and row[0] != 0:
                # 返回获胜玩家的值（1 或 -1）
                return row[0]
        # 检查列
        for col in range(3):  # 遍历列索引（0, 1, 2）
            if dict[0][col] == dict[1][col] == dict[2][col] and dict[0][col] != 0:
                # 返回获胜玩家的值（1 或 -1）
                return dict[0][col]

        # 检查对角线
        if dict[0][0] == dict[1][1] == dict[2][2] and dict[0][0] != 0:
            #print(f"玩家获胜，颜色：{'白棋' if dict[0][0] == 1 else '黑棋'}")
            return dict[0][0]
        if dict[0][2] == dict[1][1] == dict[2][0] and dict[0][2] != 0:
            #print(f"玩家获胜，颜色：{'白棋' if dict[0][2] == 1 else '黑棋'}")
            return dict[0][2]

        # 无胜利者
        return 0
def help(dict,player):
        opponent = -player  # 对手

    # 1. 检查是否有立即获胜的机会
        for i in range(3):
            for j in range(3):
                time.sleep(0.1)
                if dict[i][j] == 0:  # 空位
                    dict[i][j] = player  # 模拟下棋
                    if check_winner(dict) == player:  # 检查是否获胜
                        dict[i][j] = 0  # 恢复空位
                        return (i, j)  # 返回获胜位置
                    else:  # 不获胜
                        dict[i][j] = 0  # 恢复空位

        # 2. 检查是否需要阻止对手获胜
        for i in range(3):
            for j in range(3):
                time.sleep(0.1)
                if dict[i][j] == 0:  # 空位
                    dict[i][j] = opponent  # 模拟对手下棋
                    if check_winner(dict) == opponent:  # 检查对手是否获胜
                        dict[i][j] = 0  # 恢复空位
                        return (i, j)  # 返回阻止位置
                    else:  # 不获胜
                        dict[i][j] = 0  # 恢复空位

        # 3. 优先占据中心
        if dict[1][1] == 0:  # 中心为空
            return (1, 1)

        if dict[1][1] == player and dict[1][0] == opponent and all(dict[i][j] == 0 for i in range(3) for j in range(3) if (i, j) not in [(1, 1), (1, 0)]):  # 中心为白棋，且左边为空
            return (0,2)
        if dict[1][1] == player and dict[1][2] == opponent and all(dict[i][j] == 0 for i in range(3) for j in range(3) if (i, j) not in [(1, 1), (1, 2)]):  # 中心为白棋，且右边为空
            return (0,0)
        if dict[1][1] == player and dict[0][1] == opponent and all(dict[i][j] == 0 for i in range(3) for j in range(3) if (i, j) not in [(1, 1), (0, 1)]):  # 中心为白棋，且上边为空
            return (2,0)
        if dict[1][1] == player and dict[2][1] == opponent and all(dict[i][j] == 0 for i in range(3) for j in range(3) if (i, j) not in [(1, 1), (2, 1)]):  # 中心为白棋，且下边为空
            return (0,0)
            
        # 4. 优先占据角落
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for (i, j) in corners:
            if dict[i][j] == 0:  # 角落为空
                return (i, j)

        # 5. 占据剩余的空位
        for i in range(3):
            for j in range(3):
                if dict[i][j] == 0:  # 空位
                    return (i, j)

        # 如果没有空位，返回 None
        return None
