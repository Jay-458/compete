import cv2
import numpy as np

def split_quadrilateral_into_grid(vertices):
    """
    将四边形分割成九宫格，并计算每个格子的中心坐标。

    参数:
        vertices: 四边形的四个顶点，形状为 (4, 2) 的 NumPy 数组，顺序为：左上、右上、右下、左下。

    返回:
        grid_centers: 九宫格每个格子的中心坐标，形状为 (3, 3, 2) 的 NumPy 数组。
    """
    # 确保顶点顺序正确（左上、右上、右下、左下）
    tl, tr, br, bl = vertices  # top-left, top-right, bottom-right, bottom-left

    # 初始化九宫格中心坐标
    grid_centers = np.zeros((3, 3, 2), dtype=np.int32)

    # 遍历九宫格的每个格子
    for i in range(3):
        for j in range(3):
            # 计算水平和垂直方向上的插值比例
            u = (j + 0.5) / 3  # 水平方向比例
            v = (i + 0.5) / 3  # 垂直方向比例

            # 计算上边和下边的插值点
            top = tl + (tr - tl) * u  # 上边点
            bottom = bl + (br - bl) * u  # 下边点

            # 计算当前格子的中心点
            center = top + (bottom - top) * v
            grid_centers[i][j] = center

    return grid_centers
def findground(image):
    # 调整图像大小
    image = cv2.resize(image, (720, 480))
    
    # 转为灰度图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 二值化
    _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
    
    # 膨胀操作
    kernel = np.ones((10, 10), np.uint8)
    dilated_image = cv2.dilate(binary_image, kernel, iterations=1)
    
    # 查找轮廓
    contours, _ = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 获取最大轮廓（假设只有一个正方形）
    square_contour = max(contours, key=cv2.contourArea)
    if square_contour is not None:
        
        epsilon = 0.02 * cv2.arcLength(square_contour, True)  # 近似精度
        approx = cv2.approxPolyDP(square_contour, epsilon, True)
        
        min_length = float('inf')

    # 遍历近似多边形的所有边
        for i in range(len(approx)):
            # 获取当前顶点和下一个顶点（如果是最后一个顶点，则下一个顶点为第一个顶点）
            current_point = approx[i][0]
            next_point = approx[(i + 1) % len(approx)][0]

            # 计算两点之间的距离（边的长度）
            length = np.sqrt((current_point[0] - next_point[0]) ** 2 + (current_point[1] - next_point[1]) ** 2)

            # 更新最短边长度
            if length < min_length:
                min_length = length
        BOARD_SIZE = min_length
        GRID_SIZE = int(BOARD_SIZE // 3)
        # 确保轮廓是四边形
        if len(approx) == 4:
            # 将顶点坐标转换为整数
            vertices = np.intp(approx)
            grid_centers = split_quadrilateral_into_grid(vertices)
            #print(grid_centers)
            # 方法 1：使用 cv2.drawContours() 绘制轮廓
            cv2.drawContours(image, [vertices], -1, (0, 255, 0), 3)

            # 方法 2：使用 cv2.polylines() 绘制轮廓
            # cv2.polylines(image, [vertices], isClosed=True, color=(0, 255, 0), thickness=3)

            # 在图像上标出四个顶点
            for i, vertex in enumerate(vertices):
                x, y = vertex.ravel()
                cv2.circle(image, (x, y), 5, (0, 0, 255), -1)  # 画点
                cv2.putText(image, f"P{i+1}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

            for i in range(3):
                for j in range(3):
                    x, y = grid_centers[i, j]
                    cv2.circle(image, (x, y), 5, (0, 255, 0), -1)  # 画点
                    cv2.putText(image, f"({i},{j})", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, ())
            # 显示结果
            #cv2.imshow('Contour with 4 Vertices', image)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
        
        return {
            "grid_centers": grid_centers,
            "BOARD_SIZE": BOARD_SIZE,
            "GRID_SIZE": GRID_SIZE
        }
    return None


    
        
'''
if __name__ == "__main__":
    # 可动参数
    img_path = "D:\\AK48\\Documents\\yy_brold.jpg"
    img = cv2.imread(img_path)
    a = findground(img)
    
    print(f"棋盘大小: {a['BOARD_SIZE']}")
    print(f"格子大小: {a['GRID_SIZE']}")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(a)
'''
if __name__ == "__main__":
    # 可动参数
    img_path = "D:\\AK48\\Pictures\\Camera Roll\\WIN_20250326_15_18_14_Pro.jpg"
    img = cv2.imread(img_path)
    dict = findground(img)
    #centers = dict['grid_centers']
    #print(centers[0][0])
    #x, y = centers[0][0]
    #print(x, y)
    #findground(img)
    GRID_SIZE = dict['GRID_SIZE']
    print(GRID_SIZE)

    

