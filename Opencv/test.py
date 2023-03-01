#coding: utf-8
import cv2
import numpy as np
import imutils


im = cv2.imread('C:/Users/szh/Desktop/szh/Python_test/Opencv/11.jpg')
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)  # 大津阈值
img=cv2.bitwise_not(thresh)
cnts,_ = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)  #cv2.RETR_EXTERNAL 定义只检测外围轮廓
#print(contours)
#cnts = contours[0] if imutils.is_cv2() else contours[1]  #用imutils来判断是opencv是2还是2+
# print(cnts)
#cnt=np.concatenate((cnts[0],cnts[1],cnts[2],cnts[3]),axis=0)
# if len(cnts)==1:
    # cnt=cnts[0]
# else:
    # cnt=np.concatenate((cnts),axis=0)
    
lst1=[]
# lst2=[]
# for i in range(len(cnts)):
    # print(len(cnts[i]))
    # if len(cnts[i])>400:
        # lst1.append(cnts[i])
    # else:
        # lst2.append(cnts[i])
# cnt=np.concatenate((lst1),axis=0)
# 外接矩形框，没有方向角
#im=remove(im,lst2)
for i in range(len(cnts)):
    x, y, w, h = cv2.boundingRect(cnts[i])
    if w>50:
        #cv2.rectangle(im, (x-1, y-1), (x + w + 1, y + h + 1), (0, 255, 0), 1)
        lst1.append(cnts[i])
    else:
        im[y:y+h,x:x+w]=255
cnt=np.concatenate((lst1),axis=0)
hull = cv2.convexHull(cnt)
length = len(hull)
cv2.fillPoly(im, [hull], (0,0,0))
im=cv2.bitwise_not(im)
# for i in range(len(hull)):
    # cv2.line(im, tuple(hull[i][0]), tuple(hull[(i+1)%length][0]), (0,0,0), 1)
x, y, w, h = cv2.boundingRect(cnt)       
cv2.rectangle(im, (x-1, y-1), (x + w + 1, y + h + 1), (0, 255, 0), 1)
# 最小外接矩形框，有方向角
# rect = cv2.minAreaRect(cnt)
# box = cv2.cv.Boxpoints() if imutils.is_cv2()else cv2.boxPoints(rect)
# box = np.int0(box)
# cv2.drawContours(im, [box], 0, (0, 0, 255), 2)

# 最小外接圆
# (x, y), radius = cv2.minEnclosingCircle(cnt)
# center = (int(x), int(y))
# radius = int(radius)
# print('圆心',center)
# print('半径',radius)
# cv2.circle(im, center, radius, (255, 0, 0), 2)
# cv2.circle(im, center, 5, (0, 0, 255), -1)

# 椭圆拟合
# ellipse = cv2.fitEllipse(cnt)
# cv2.ellipse(im, ellipse, (255, 255, 0), 2)
# print(ellipse)

# 直线拟合
# rows, cols = im.shape[:2]
# [vx, vy, x, y] = cv2.fitLine(cnt, cv2.DIST_L2, 0, 0.01, 0.01)
# lefty = int((-x * vy / vx) + y)
# righty = int(((cols - x) * vy / vx) + y)
# im = cv2.line(im, (cols - 1, righty), (0, lefty), (0, 255, 255), 2)

cv2.imshow('a',im)
#cv2.imwrite('C:/Users/szh/Desktop/szh/Python_test/Opencv/11_result1.jpg',im)
cv2.waitKey(0)