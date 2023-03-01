from PyQt5.QtWidgets import *
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtGui import *

import sys
class A(QWidget):
    def __init__(self):
        super(A,self).__init__()
        self.setFixedSize(400,500)
        self.layout=QGridLayout(self)
        self.btn=QPushButton('添加')
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)
        self.btn.clicked.connect(self.btn1)

    def btn1(self):
        label={}
        ok,f=QFileDialog.getOpenFileNames(self,'打开','/','png(*.png)')
        for i,j in enumerate(ok):
            label[i]=QLabel(str(i))
            label[i].setFixedSize(100,100)
            self.layout.addWidget(label[i])
            pix=QPixmap(j)
            label[i].setPixmap(pix)
            self.resize(pix.width(),pix.height())

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = A()
    win.show()
    sys.exit(app.exec_())