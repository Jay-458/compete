import cv2
import numpy as np
import math

class Detector:
    def __init__(self):
        self.img = None
        self.white_chess = []
        self.black_chess = []

    def find_roi(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # 黄色的HSV范围
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([40, 255, 255])
        # 创建掩膜
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        # 创建膨胀核，可以根据需求调整大小和形状
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
        # 对掩膜进行膨胀
        dilated_mask = cv2.dilate(mask, kernel, iterations=1)
        contours, _ = cv2.findContours(dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 遍历每个轮廓，过滤面积小于5000的
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 5000:
                continue  # 跳过面积小于5000的轮廓

            rect = cv2.minAreaRect(cnt)  # 计算最小旋转外接矩形
            box = cv2.boxPoints(rect)    # 获取矩形4个角点
            up_left = box[0]
            up_right = box[3]
            down_left = box[1]
            down_right = box[2]

            # 计算边上六等分点（每条边5个点）
            def get_divided_points(p1, p2, divisions=6):
                points = []
                for i in range(1, divisions):
                    t = i / divisions
                    point = (1 - t) * p1 + t * p2
                    if i in [1,3,5]:
                        points.append(point.astype(int))
                return points

            top_points = get_divided_points(up_left, up_right)
            right_points = get_divided_points(up_right, down_right)
            bottom_points = get_divided_points(down_right, down_left)
            left_points = get_divided_points(down_left, up_left)


            # 按 x 坐标升序排序
            top_points_sorted = sorted(top_points, key=lambda p: p[0])
            bottom_points_sorted = sorted(bottom_points, key=lambda p: p[0])

            # 按 y 坐标升序排序
            left_points_sorted = sorted(left_points, key=lambda p: p[1])
            right_points_sorted = sorted(right_points, key=lambda p: p[1])

             # 形成3条水平线和3条垂直线
            horizontal_lines = list(zip(top_points_sorted, bottom_points_sorted))
            vertical_lines = list(zip(left_points_sorted, right_points_sorted))

            def line_intersection(p1, p2, p3, p4):
                """计算两条线段p1-p2和p3-p4的交点，若无交点返回None"""
                p1, p2, p3, p4 = map(np.array, (p1, p2, p3, p4))
                s1 = p2 - p1
                s2 = p4 - p3
                denom = -s2[0] * s1[1] + s1[0] * s2[1]
                if denom == 0:
                    return None
                s = (-s1[1] * (p1[0] - p3[0]) + s1[0] * (p1[1] - p3[1])) / denom
                t = ( s2[0] * (p1[1] - p3[1]) - s2[1] * (p1[0] - p3[0])) / denom
                if 0 <= s <= 1 and 0 <= t <= 1:
                    return p1 + t * s1
                return None

            crossing_pts = []
            # 求3*3条线两两交点，共9个
            for h_start, h_end in horizontal_lines:
                for v_start, v_end in vertical_lines:
                    pt = line_intersection(h_start, h_end, v_start, v_end)
                    if pt is not None:
                        pt_int = pt.astype(int)
                        crossing_pts.append(pt_int)

            crossing_pts_sorted = sorted(crossing_pts, key=lambda p: (-p[1], p[0]))
            # 画交点（黄色圆圈）
            if len(crossing_pts_sorted) >= 1:
                # for idx, pt_int in enumerate(crossing_pts_sorted):
                #     # 绘制圆点，黄色，半径7，线宽3
                #     cv2.circle(img, tuple(pt_int), 7, (0, 255, 255), 3)

                #     # 绘制坐标文字。字符串格式为 "(x,y)"
                #     text = f"({pt_int[0]}, {pt_int[1]})"

                #     # 文字位置稍微偏右下方，避免被圆点遮挡
                #     text_pos = (pt_int[0] + 10, pt_int[1] + 10)

                #     # 使用拟合矩形字体，字体大小0.5，颜色黄色，线宽1
                #     cv2.putText(img, text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
                for idx, pt_int in enumerate(crossing_pts_sorted, start=1):  # 从1开始编号更直观
                    # 绘制圆点，黄色，半径7，线宽3
                    cv2.circle(img, tuple(pt_int), 7, (0, 255, 255), 3)

                    # 绘制序号和坐标，格式如 "1: (x, y)"
                    text = f"{idx}: ({pt_int[0]}, {pt_int[1]})"

                    # 文字位置，点的右下方偏移
                    text_pos = (pt_int[0] + 10, pt_int[1] + 10)

                    # 绘制文字
                    cv2.putText(img, text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
            else:
                  crossing_pts_sorted = []
            return img, []


if __name__ == '__main__':

    cap = cv2.VideoCapture(1)

    detector = Detector()
    if not cap.isOpened():
        print("摄像头无法打开！")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        yellow, list = detector.find_roi(frame)
        print(list)
        cv2.imshow("Frame with Yellow Rectangle and Grid", yellow)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
