import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 365, 500)
        self.label = QtWidgets.QLabel()
        #self.label.setStyleSheet("background-color: rgb(221, 221, 221);")
        canvas = QtGui.QPixmap(300, 300)
        canvas.fill(QtGui.QColor("white"))
        self.label.setPixmap(canvas)#创建canvas，并加入label作为画板。
        self.setCentralWidget(self.label)
        self.draw_something()#绘图函数

    def draw_something(self):
        painter = QtGui.QPainter(self.label.pixmap())
        brush=QtGui.QBrush()#添加画笔
        brush.setColor(QtGui.QColor("blue"))
        brush.setStyle(Qt.SolidPattern)#纯色背景
        painter.setBrush(brush)
        painter.drawRect(100,100,50,50)#矩形坐标+尺寸
        painter.drawRect(150,150,50,50)
        painter.end()

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
