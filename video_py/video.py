import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier('D:/AI/OpenCV/data/haarcascades/haarcascade_frontalface_default.xml')
def ellipse_detect(img):
    #img = cv2.imread(image,cv2.IMREAD_COLOR)
    skinCrCbHist = np.zeros((256,256), dtype= np.uint8 )
    cv2.ellipse(skinCrCbHist ,(113,155),(23,15),43,0, 360, (255,255,255),-1)
    
    faces = face_cascade.detectMultiScale(img, 1.3, 5)
    for (x,y,w,h) in faces:
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,0),-1)
    YCRCB = cv2.cvtColor(img,cv2.COLOR_BGR2YCR_CB)
    (y,cr,cb)= cv2.split(YCRCB)
    skin = np.zeros(cr.shape, dtype=np.uint8)
    (x,y)= cr.shape
    for i in range(0,x):
        for j in range(0,y):
            CR= YCRCB[i,j,1]
            CB= YCRCB[i,j,2]
            if skinCrCbHist [CR,CB]>0:
                skin[i,j]= 255
    #cv2.namedWindow(image, cv2.WINDOW_NORMAL)
    #cv2.imshow(image, img)
    dst = cv2.bitwise_and(img,img,mask= skin)
    '''faces = face_cascade.detectMultiScale(dst, 1.3, 5)
    for (x,y,w,h) in faces:
        dst = cv2.rectangle(dst,(x,y),(x+w,y+h),(0,0,0),-1)'''
    cv2.namedWindow("cutout", cv2.WINDOW_NORMAL)
    cv2.imshow("cutout",dst)
    #cv2.waitKey()


def video_demo():
    capture = cv2.VideoCapture(0)#0为电脑内置摄像头
    while(True):
        ret,frame = capture.read()#摄像头读取,ret为是否成功打开摄像头,true,false。 frame为视频的每一帧图像
        frame = cv2.flip(frame,1)#摄像头是和人对立的，将图像左右调换回来正常显示。
        cv2.imshow("window",frame)
        ellipse_detect(frame)
        if cv2.waitKey(1) &0xFF == ord(' '):  #按空格键退出
            break

#ellipse_detect('C:/Users/szh/Desktop/szh/Python test/video_py/1.jpg')
video_demo()
cv2.destroyAllWindows()
