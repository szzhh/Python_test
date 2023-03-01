import cv2
from math import ceil
import numpy as np


# 图像resize
def deal(data):
    dsize = 400
    height = data.shape[0]
    width = data.shape[1]
    # 设置最小的文字像素高度
    min_val = 1

    start_i = -1
    end_i = -1
    # 存放每行的起止坐标
    rowinfo = []

    # 行分割
    for i in range(height):
        # 行中有字相关信息
        if (not data[i].all()):
            end_i = i
            if(start_i < 0):
                start_i = i
                pass
        # 行中无字相关信息
        elif (data[i].all() and start_i >= 0):
            if(end_i - start_i >= min_val):
                rowinfo.append((start_i, end_i))
                pass
            start_i, end_i = -1, -1
    #print(rowinfo)
    # 列分割
    start_j = -1
    end_j = -1
    # 最小文字像素宽度
    min_val_word = 1
    # 分割后保存编号
    number = 0
    for start, end in rowinfo:
        for j in range(width):
            # 列中有字相关信息
            if(not data[start: end, j].all()):
                end_j = j
                if(start_j < 0):
                    start_j = j
                    pass
            # 列中无字信息
            elif(data[start: end, j].all() and start_j >= 0):
                if(end_j - start_j >= min_val_word):
                    start=start
                    end=end+1
                    start_j=start_j
                    end_j=end_j+1
                    img_deal = data[start:end, start_j: end_j]
                    top=start
                    bottom=dsize-end
                    left=start_j
                    right=dsize-end_j
                    centerh=int((start+end)/2)
                    centerw=int((start_j+end_j)/2)
                    number += 1
                    pass
                start_j, end_j = -1, -1
    return img_deal,top,bottom,left,right,centerh,centerw

def image_binarization(img):
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    retval, dst = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY |cv2.THRESH_OTSU)
    return dst
        

def image_processing(img_model, img):
    imgg_model,top,bottom,left,right=deal(img_model)
    imgg,_,_,_,_=deal(img)
    size=imgg_model.shape
    img_new = cv2.resize(imgg,(size[1],size[0]))
    img_new = cv2.copyMakeBorder(img_new,top,bottom,left,right,cv2.BORDER_CONSTANT,value=[255,255,255])
    return img_new
    
def image_processing1(img_model, img):
    imgg_model,top,bottom,left,right,center_h,center_w=deal(img_model)
    imgg,_,_,_,_,_,_=deal(img)
    size=imgg_model.shape
    size1=imgg.shape
    newwidth=ceil(size1[1]*size[0]/size1[0])
    #newwidth=size[1]
    newheight=size[0]
    img_new = cv2.resize(imgg,(newwidth,newheight))
    left=ceil(left+(size[1]-newwidth)/2)
    right=ceil(right+(size[1]-newwidth)/2)
    img_new = cv2.copyMakeBorder(img_new,top,bottom,left,right,cv2.BORDER_CONSTANT,value=[255,255,255])
    return img_new

def image_processing2(img_model, img):
    imgg_model,top,bottom,left,right,center_h,center_w=deal(img_model)
    imgg,_,_,_,_,_,_=deal(img)
    size=imgg_model.shape
    size1=imgg.shape
    newwidth=ceil(size1[1]*size[0]/size1[0])
    #newwidth=size[1]
    newheight=size[0]
    img_new = cv2.resize(imgg,(newwidth,newheight))
    size2=img_new.shape
    top=int((400-size2[0])/2)
    bottom=top
    left=int((400-size2[1])/2)
    right=left
    img_new = cv2.copyMakeBorder(img_new,top,bottom,left,right,cv2.BORDER_CONSTANT,value=[255,255,255])
    return img_new

def image_processing3(img_model, img):
    img_model=image_binarization(img_model)
    img=image_binarization(img)
    imgg_model,top,bottom,left,right,center_h,center_w=deal(img_model)
    imgg,_,_,_,_,_,_=deal(img)
    size=imgg_model.shape
    size1=imgg.shape
    newwidth=ceil(size1[1]*size[0]/size1[0])
    newheight=size[0]
    img_new = cv2.resize(imgg,(newwidth,newheight))
    size2=img_new.shape
    top=int(center_h-size2[0]/2)
    bottom=400-top-size2[0]
    left=int(center_w-size2[1]/2)
    right=400-left-size2[1]
    img_new = cv2.copyMakeBorder(img_new,top+10,bottom-10,left,right,cv2.BORDER_CONSTANT,value=[255,255,255])
    return img_new

path1 = 'D:/AI/Mnist/1_template.jpg'
path2 = 'D:/AI/Mnist/1.png'
root = 'D:/AI/Mnist/output/'
img_model = cv2.imread(path1,cv2.IMREAD_GRAYSCALE)
img = cv2.imread(path2,cv2.IMREAD_GRAYSCALE)
image_processed = image_processing3(img_model, img)
image_processed=image_binarization(image_processed)
img_model=image_binarization(img_model)
where_1 = np.where(image_processed[:200,:200] == 0)
where_2 = np.where(image_processed[:200,200:] == 0)
where_3 = np.where(image_processed[200:,:200] == 0)
where_4 = np.where(image_processed[200:,200:] == 0)
print(len(where_1[0]),len(where_2[0]),len(where_3[0]),len(where_4[0]))
img_sub=image_processed-img_model
cv2.imshow('Show1',img_model)
cv2.imshow('Show2',img)
cv2.imshow('Show3',image_processed)
cv2.imshow('Show4',img_sub)
cv2.waitKey(0)
