import os
import sys
import  cv2
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2 import QtCore, QtGui, QtWidgets
import time
from matplotlib import pyplot as plt
from PIL import Image, ImageQt
from Ui_mainwindow_1 import Ui_Form
#import vtk_first_try

global path
path=os.path.split(os.path.realpath(__file__))[0]+'/0.bmp'

class L(QLabel):
    def __init__(self, parent):
        global path
        super().__init__(parent=parent)
        self.setStyleSheet('QFrame {background-color:black;}')
        self.setGeometry(QtCore.QRect(289, 159, 780, 780))
        self.img = ImageQt.toqpixmap(Image.fromarray(cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)))
        self.scaled_img = self.img.scaled(self.size())
        self.point = QPoint(0, 0)
        self.lastPos= QPoint(self.width()/2,self.height()/2)#十字线复原
    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        self.draw_img(painter)
        self.line(painter)
        painter.end()
        
    def line(self,painter):
        pen=QPen()
        pen.setWidth(2)
        pen.setStyle(Qt.DashDotLine)
        pen.setColor(Qt.blue)
        painter.setPen(pen)
        painter.drawLine(0, self.lastPos.y(), self.width(), self.lastPos.y())
        painter.drawLine(self.lastPos.x(), 0, self.lastPos.x(), self.height())
        
    def draw_img(self, painter):
        painter.drawPixmap(self.point, self.scaled_img)

    def mouseMoveEvent(self, e):  # 重写移动事件
        if self.left_click:
            self._endPos = e.pos() - self._startPos
            self.point = self.point + self._endPos
            self._startPos = e.pos()
            self.lastPos=e.pos()
            self.repaint()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.left_click = True
            self._startPos = e.pos()
            self.lastPos=e.pos()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.lastPos=e.pos()
            #self.left_click = False
            self.repaint()
        elif e.button() == Qt.RightButton:
            self.point = QPoint(0, 0)
            self.scaled_img = self.img.scaled(self.size())
            self.lastPos= QPoint(self.width()/2,self.height()/2)
            self.repaint()

    def wheelEvent(self, e):
        if e.angleDelta().y() > 0:
            # 放大图片
            self.scaled_img = self.img.scaled(self.scaled_img.width()-20, self.scaled_img.height()-20)
            new_w = e.x() - (self.scaled_img.width() * (e.x() - self.point.x())) / (self.scaled_img.width() + 20)
            new_h = e.y() - (self.scaled_img.height() * (e.y() - self.point.y())) / (self.scaled_img.height() + 20)
            self.point = QPoint(new_w, new_h)
            self.repaint()
        elif e.angleDelta().y() < 0:
            # 缩小图片
            self.scaled_img = self.img.scaled(self.scaled_img.width()+20, self.scaled_img.height()+20)
            new_w = e.x() - (self.scaled_img.width() * (e.x() - self.point.x())) / (self.scaled_img.width() - 20)
            new_h = e.y() - (self.scaled_img.height() * (e.y() - self.point.y())) / (self.scaled_img.height() - 20)
            self.point = QPoint(new_w, new_h)
            self.repaint()

    def resizeEvent(self, e):
        if self.parent is not None:
            self.scaled_img = self.img.scaled(self.size())
            self.point = QPoint(0, 0)
            self.update()

class Mainwindow(QWidget):
    def __init__(self):
        super().__init__()
        self.label=L(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.phone)
        self.ui.pushButton_3.clicked.connect(self.deal)
        self.ui.pushButton_9.clicked.connect(self.help)
    def phone(self):
        QMessageBox.about(self,'联系电话','联系电话')
    def help(self):
        QMessageBox.about(self,'帮助','帮助')
    def deal(self):
        global path
        #path= (QtWidgets.QFileDialog.getOpenFileName(None, '浏览', 'D:'))[0]
        path=os.path.split(os.path.realpath(__file__))[0]+'/csu.png'
        '''img=Image.fromarray(cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB))
        self.ui.label_8.setPixmap(ImageQt.toqpixmap(img.resize((self.ui.label_8.width(), self.ui.label_8.height()))))'''
        self.label.point = QPoint(0, 0)
        self.label.img=ImageQt.toqpixmap(Image.fromarray(cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)))
        self.label.scaled_img = self.label.img.scaled(self.label.size())
        self.label.repaint()
        #self.label=L(self)
        #self.label.update()
        #self.layout.addWidget(self.label)
        
        #QApplication.processEvents()
        #mainwindow.close()
        #mainwindow=Mainwindow()
        #mainwindow.show()
if __name__ == '__main__':
    global mainwindow
    app = QApplication([])
    app.setWindowIcon(QIcon(os.path.split(os.path.realpath(__file__))[0]+'/csu.png'))
    mainwindow=Mainwindow()
    mainwindow.show()
    app.exec_()