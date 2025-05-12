import numpy as np

# 坐标系一的点
# x1 = [264, 135, 392, 400, 237]
# y1 = [190, 203, 354, 78, 379]

# # 坐标系二的点
# x2 = [-6.6, -2.3, -10.7, -11.10, -6.20]
# y2 = [9.6, 10.3, 14.9, 5.49, 15.60]

x1 = [535, 460, 221, 260, 405]
y1 = [132, 215, 97, 283, 206]

# 坐标系二的点
x2 = [2.59, 5.49, 19.69, 17.59, 7.09]
y2 = [12.39, 17.29, 15.59, 24.70, 16.49]

# 最小二乘法拟合x方向参数
A_x = np.vstack([x1, np.ones(len(x1))]).T
s_x, t_x = np.linalg.lstsq(A_x, x2, rcond=None)[0]

# 最小二乘法拟合y方向参数
A_y = np.vstack([y1, np.ones(len(y1))]).T
s_y, t_y = np.linalg.lstsq(A_y, y2, rcond=None)[0]

# 转换函数
def convert_coordinate(point):
    x2 = s_x * point[0] + t_x
    y2 = s_y * point[1] + t_y
    return (round(x2, 2), round(y2, 2))# round表示四舍五入，保留两位小数

if __name__ == '__main__':
    result = convert_coordinate([221,97])
    print(result)
'''
# 测试
points_1 = [(264, 190), (135, 203), (392, 354), (400, 78), (237, 379),(271,242)]
points_2 = [convert_coordinate(x, y) for x, y in points_1]

print("拟合参数:")
print(f"s_x = {s_x}, t_x = {t_x}")
print(f"s_y = {s_y}, t_y = {t_y}")
print("\n转换结果:")
for p1, p2 in zip(points_1, points_2):
    print(f"坐标系一: {p1} -> 坐标系二: {p2}")
'''