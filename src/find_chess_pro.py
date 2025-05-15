import cv2
import numpy as np

def draw_chessboard(image,blackchesses,whitechesses):
    for blackchess in blackchesses :
        #cv2.drawContours(image, [blackchess], -1, (0, 255, 0), 2)
        cv2.circle(image, (blackchess[0], blackchess[1]), 5, (0, 0, 255), -1)
        cv2.putText(image, f"({blackchess[0]}, {blackchess[1]})", (blackchess[0] - 20, blackchess[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    for whitechess in whitechesses :
        #cv2.drawContours(image, [whitechess], -1, (0, 255, 0), 2)
        cv2.circle(image, (whitechess[0], whitechess[1]), 5, (0, 255, 0), -1)
        cv2.putText(image, f"({whitechess[0]}, {whitechess[1]})", (whitechess[0] - 20, whitechess[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        
def classify_background_chess_color(img, contours):
    black_chesses = []
    white_chesses = []
    for contour in contours:
        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, -1)  # 填充轮廓以获取颜色
        mean_val = cv2.mean(img, mask=mask)  # 计算平均色彩

        # 判断颜色是否接近黑色或白色
        if mean_val[0] < 100 and mean_val[1] < 100 and mean_val[2] < 100:  # 接近黑色
            black_chesses.append(contour)
        else:
            white_chesses.append(contour)

    return black_chesses, white_chesses

def contours_to_positom(contours):
    """ 将轮廓转换为棋子位置 """

    contours_positions = []

    for contour in contours:
        M = cv2.moments(contour)  # 计算轮廓的中心点
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            contours_positions.append((cX, cY))

    return contours_positions
def findchess(frame):
    lower_blue = np.array([88, 64, 89])  # 蓝色的下界
    upper_blue = np.array([180, 255, 255]) 
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    inverse_mask = cv2.bitwise_not(mask)
    cv2.imshow('inverse_mask',inverse_mask)
    contours, _ = cv2.findContours(inverse_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    chesses_contours = []
    for cnt in contours:
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        area = cv2.contourArea(cnt)
        circle_area = np.pi * (radius ** 2)
        if circle_area == 0:
            continue
        # 轮廓面积与外接圆面积之比（接近1则是圆）
        ratio = area / circle_area
        if ratio > 0.8 and cv2.contourArea(cnt) > 1000 and cv2.contourArea(cnt) < 2000:
            chesses_contours.append(cnt)

    black_contours, white_contours = classify_background_chess_color(frame, chesses_contours)  # 按颜色分类
    cv2.drawContours(frame,  black_contours, -1, (0, 0, 255), 3)
    cv2.drawContours(frame,  white_contours, -1, (0, 255, 0), 3)
    blackchess_list = contours_to_positom(black_contours)  # 获取黑棋子位置
    whitechess_list = contours_to_positom(white_contours)  # 获取白棋子位置
    draw_chessboard(frame,blackchess_list,whitechess_list)
    # print(blackchess_list)
    # print(whitechess_list)
    # for cnt in new_contours:
    #     (x, y), radius = cv2.minEnclosingCircle(cnt)
    #     area = cv2.contourArea(cnt)
    #     circle_area = np.pi * (radius ** 2)
    #     if circle_area == 0:
    #         continue
    #     # 轮廓面积与外接圆面积之比（接近1则是圆）
    #     ratio = area / circle_area
    #     if ratio > 0.8:  # 阈值
    #         chesses.append(cnt)
    # cv2.drawContours(frame, chesses, -1, (0, 255, 0), 3)
    return blackchess_list,whitechess_list

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        findchess(frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break