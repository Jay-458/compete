import cv2
import numpy as np
def findwhite(image):
    copyimage = image
    chess_area_min = 3000
    chess_area_max = 4000
    
 #灰度化，二值化  
    gray_image = cv2.cvtColor(copyimage, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 140, 255, cv2.THRESH_BINARY)
    

    mask = binary_image
    result = cv2.bitwise_and(copyimage, copyimage, mask=mask)
    
# 找到轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    whitechesses = [whitechess for whitechess in contours if cv2.contourArea(whitechess)>chess_area_min and cv2.contourArea(whitechess)<chess_area_max ]
#创建两个列表，分别记录白色棋子的x轴坐标和y轴坐标
    
    whitechess_list = []
#计算中心坐标
    for whitechess in whitechesses :

        M = cv2.moments(whitechess)
        
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            
        else:
            cX, cY = 0, 0
        whitechessX_Y = []
        whitechessX_Y.append(cX)
        whitechessX_Y.append(cY)
        whitechess_list.append(whitechessX_Y)
        # 在图像上绘制轮廓和中心
        cv2.drawContours(copyimage, [whitechess], -1, (0, 255, 0), 2)
        cv2.circle(copyimage, (cX, cY), 5, (0, 0, 255), -1)
        cv2.putText(copyimage, f"({cX}, {cY})", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.drawContours(copyimage, contours, -1, (0, 255, 0), 2)
        
    
    #cv2.imshow('result', copyimage)
    #cv2.imshow('grey',gray_image)
    #print(whitechess_list)
    
    #返回坐标
    return whitechess_list

'''
if __name__ == "__main__":
    # 可动参数
    img_path = "D:\\Users\\AK48\\Pictures\\Screenshots\\white chess.jpg"
    a,b = findwhite(img_path)
    print(a,b)
    cv2.waitKey(0)
    cv2.destroyAllWindows()         
'''    

