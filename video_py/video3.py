import numpy as np
import cv2

def video_capture():
    cap = cv2.VideoCapture(0)
    while True:
        # capture frame-by-frame
        ret,frame = cap.read()
        # our operation on the frame come here
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 可选择灰度化
        # display the resulting frame
        frame = cv2.flip(frame,1)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord(' '): # 按空格键退出
            break
    # when everything done , release the capture
    cap.release()
    cv2.destroyAllWindows()

def ellipse_detect(img):
    # 椭圆肤色检测模型
    skinCrCbHist = np.zeros((256, 256), dtype=np.uint8)
    cv2.ellipse(skinCrCbHist, (113, 155), (23, 15), 43, 0, 360, (255, 255, 255), -1)
    YCRCB = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    (y, cr, cb) = cv2.split(YCRCB)
    skin = np.zeros(cr.shape, dtype=np.uint8)
    (x, y) = cr.shape
    for i in range(0, x):
        for j in range(0, y):
            CR = YCRCB[i, j, 1]
            CB = YCRCB[i, j, 2]
            if skinCrCbHist[CR, CB] > 0:
                skin[i, j] = 255
    dst = cv2.bitwise_and(img, img, mask=skin)
    return dst