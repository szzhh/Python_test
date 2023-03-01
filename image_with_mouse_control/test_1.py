import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import QPainter, QColor, QBrush
from PySide2 import QtCore, QtGui, QtWidgets
import cv2
from PIL import Image, ImageQt

class Labella(QLabel):

    def __init__(self, parent):
        super().__init__(parent=parent)

        self.setStyleSheet('QFrame {background-color:grey;}')
        self.setGeometry(QtCore.QRect(100, 100, 200, 200))

    def paintEvent(self, e):
        qp = QPainter(self)
        self.drawRectangles(qp)
        qp.setBrush(QColor(200, 0, 0))
        qp.drawRect(0,0,20,20)

    '''def drawRectangles(self, qp):    
        qp.setBrush(QColor(255, 0, 0, 100))
        qp.save() # save the QPainter config

        qp.drawRect(10, 15, 20, 20)

        qp.setBrush(QColor(0, 0, 255, 100))
        qp.drawRect(50, 15, 20, 20)

        qp.restore() # restore the QPainter config            
        qp.drawRect(100, 15, 20, 20)'''

class Example(QWidget):

    def __init__(self):
        super().__init__()

        label = Labella(self)
        '''path="C:/Users/szh/Desktop/image_with_mouse_control/bg.jpg"
        img=Image.fromarray(cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB))
        label.setPixmap(ImageQt.toqpixmap(img.resize((label.width(), label.height()))))'''
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Colours')
        self.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())