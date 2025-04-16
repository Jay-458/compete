import cv2
import numpy as np
def findblack(image):
    chess_area_min = 3000
    chess_area_max = 18000
    #image = cv2.imread(image_path)
    
    image = cv2.resize(image,(720,480))
#灰度化，二值化  
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 40, 255, cv2.THRESH_BINARY)
#颠倒黑白
    binary_image = cv2.bitwise_not(binary_image)
    kernel = np.ones((5, 5), np.uint8)
    
    # 腐蚀操作
    eroded_image = cv2.erode(binary_image, kernel, iterations=1)
    
    # 膨胀操作
    dilated_image = cv2.dilate(eroded_image, kernel, iterations=1)

    mask = dilated_image
    result = cv2.bitwise_and(image, image, mask=mask)
    
# 找到轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blackchesses = [blackchess for blackchess in contours if cv2.contourArea(blackchess)>chess_area_min and cv2.contourArea(blackchess)<chess_area_max ]
#创建两个列表，分别记录白色棋子的x轴坐标和y轴坐标
    blackchess_list = []
#计算中心坐标
    for blackchess in blackchesses :

        M = cv2.moments(blackchess)
        
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
        blackchessX_Y = []
        blackchessX_Y.append(cX)
        blackchessX_Y.append(cY)
        blackchess_list.append(blackchessX_Y)
        # 在图像上绘制轮廓和中心
        cv2.drawContours(image, [blackchess], -1, (0, 255, 0), 2)
        cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)
        cv2.putText(image, f"({cX}, {cY})", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
        
    
    cv2.imshow('balck_chess', image)
    #cv2.imshow('grey',binary_image)
    #cv2.waitKey(0)
    #cv2.distroyAllWindows()
    
    #返回坐标
    return blackchess_list

'''
if __name__ == "__main__":
    # 可动参数
    img_path = "D:\\Users\\AK48\\Pictures\\Screenshots\\black chess4.jpg"
    a,b = findblack(img_path)
    print(a,b)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
'''     
    

