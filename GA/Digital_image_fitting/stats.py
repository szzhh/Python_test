import os
import sys
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile,QObject, Signal, QEventLoop, QTimer
from PySide2.QtGui import  QIcon,QTextCursor
from PySide2 import QtCore, QtGui, QtWidgets
from threading import Timer
import time
from matplotlib import pyplot as plt
from PIL import Image, ImageQt
import main

#ori_img=''#os.path.split(os.path.realpath(__file__))[0]+'/0.bmp'
resume=False
n=0

class Stats:
    def __init__(self):
        # 从文件中加载UI定义
        qfile_stats=QFile(os.path.split(os.path.realpath(__file__))[0]+'/stats.ui')
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load(qfile_stats)

        self.ui.button.clicked.connect(self.setBrowerPath)
    
    def setBrowerPath(self):
        download_path = QtWidgets.QFileDialog.getOpenFileName(None, '浏览', 'D:')
        self.ui.lineEdit.setText(download_path[0])
    def gettext(self):
        global ori_img
        ori_img = self.ui.lineEdit.text()
class Wmain:
    def __init__(self):
        # 从文件中加载UI定义
        qfile_wmain=QFile(os.path.split(os.path.realpath(__file__))[0]+'/wmain.ui')
        qfile_wmain.open(QFile.ReadOnly)
        qfile_wmain.close()
        self.ui = QUiLoader().load(qfile_wmain)
        
        self.pushButton_down = False
        self.ui.pushButton_6.clicked.connect(self.read)
        self.ui.pushButton.clicked.connect(self.onButtonClick)
        self.ui.pushButton_3.clicked.connect(self.draw)
        
    def putimg(self):
        global ori_img
        jpg = QtGui.QPixmap(ori_img).scaled(self.ui.label.width(), self.ui.label.height())
        self.ui.label.setPixmap(jpg)
    def read(self):
        global resume
        resume=True
        QMessageBox.about(self.ui,'数据集生成器','存档读取成功！')
    def onButtonClick(self):
        global ori_img
        global resume
        global genes
        global generation
        global best
        global worst
        global avg
        global data
        global size
        global backup
        global n
        n+=1
        if n==1:
            backup = os.path.splitext(ori_img)[0]+'/backup.tmp'
            data, size = main.GetImage(ori_img)
            if resume and os.path.exists(backup):
                genes, generation, best, worst, avg= main.ReadData(backup)
            else:
                genes = main.RandGenes(size)
                generation = 0
                best=[]
                worst=[]
                avg=[]
        if True:
            self.ui.pushButton.setDown(not self.pushButton_down)
            self.pushButton_down=not self.pushButton_down
            self.run()

    def run(self):
        #多线程
        t=Timer(0.005,self.run)
        if self.pushButton_down==False:
            t.cancel()
        global ori_img
        global resume
        global genes
        global generation
        global best
        global worst
        global avg
        global data
        global size
        global backup
        generation += 1
        genes = main.CalcFitness(genes, data)
        fitsum=0
        for i in range (100):
            fitsum+=genes[i][1]
        Averagefit=round(float(fitsum)/100,4)
        print('Generation: {}, Best: {:.4f}, Worst: {:.4f}, Average: {:.4f}'.format(generation, genes[0][1], genes[99][1],Averagefit))
        self.ui.textEdit.append('Generation: {}, Best: {:.4f}, Worst: {:.4f}, Average: {:.4f}'.format(generation, genes[0][1], genes[99][1],Averagefit))
        self.ui.textEdit.moveCursor(QTextCursor.End)
        best.append(genes[0][1])
        worst.append(genes[99][1])
        avg.append(Averagefit)
		#draw(generation,best,worst,avg)
        genes = main.Select(genes, size)
        genes = main.Variation(genes)
        if generation % 10 == 0:
            main.SaveData({'gene': genes, 'generation': generation, 'best':best, 'worst':worst, 'avg':avg}, backup)
            main.SavePic(genes[0], generation, ori_img)
        #展示图片
        img = Image.open(ori_img)
        img = img.convert('RGB')
        for j, row in enumerate(genes[0][0]):
            for i, col in enumerate(row):
                r, g, b = col
                img.putpixel((i, j), (r, g, b))
        self.ui.label_2.setPixmap(ImageQt.toqpixmap(img.resize((self.ui.label_2.width(), self.ui.label_2.height()))))
        if self.pushButton_down==True:
            t.start()
    def draw(self):
        global generation
        global best
        global worst
        global avg
        plt.rcParams['font.sans-serif']=['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.plot(range(generation),best,color='red')
        plt.plot(range(generation),worst,color='blue')
        plt.plot(range(generation),avg,color='green')   
        plt.xlabel('进化代数')
        plt.ylabel('适应度值')
        plt.title('适应度值变化图')
        plt.legend(['Best','Worst','Average'])
        plt.show()
        #plt.ion()
        #plt.pause(0.01)


if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon(os.path.split(os.path.realpath(__file__))[0]+'/csu.png'))
    stats = Stats()
    stats.ui.show()
    wmain=Wmain()
    stats.ui.button1.clicked.connect(stats.gettext)
    stats.ui.button1.clicked.connect(wmain.putimg)
    stats.ui.button1.clicked.connect(wmain.ui.show)
    wmain.ui.pushButton_4.clicked.connect(stats.ui.show)
    app.exec_()