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

path="C:/Users/szh/Desktop/image_with_mouse_control/bg.jpg"

class L(QLabel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.img = ImageQt.toqpixmap(Image.fromarray(cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)))
        self.scaled_img = self.img.scaled(self.size())
        self.point = QPoint(0, 0)
        self.setStyleSheet('QFrame {background-color:grey;}')
        self.setGeometry(QtCore.QRect(40, 40, 381, 291))

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        self.draw_img(painter)
        painter.end()

    def draw_img(self, painter):
        painter.drawPixmap(self.point, self.scaled_img)

    def mouseMoveEvent(self, e):  # 重写移动事件
        if self.left_click:
            self._endPos = e.pos() - self._startPos
            self.point = self.point + self._endPos
            self._startPos = e.pos()
            self.repaint()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.left_click = True
            self._startPos = e.pos()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.left_click = False
        elif e.button() == Qt.RightButton:
            self.point = QPoint(0, 0)
            self.scaled_img = self.img.scaled(self.size())
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
        qfile_stats=QFile(os.path.split(os.path.realpath(__file__))[0]+'/test.ui')
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()
        self.ui = QUiLoader().load(qfile_stats)
        self.label=L(self)
if __name__ == '__main__':
    app = QApplication([])
    #app.setWindowIcon(QIcon(os.path.split(os.path.realpath(__file__))[0]+'/csu.png'))
    mainwindow=Mainwindow()
    mainwindow.show()
    app.exec_()