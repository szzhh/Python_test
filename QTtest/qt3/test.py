#!/usr/bin/env python3
# -*- coding:utf-8 -*- 
from PyQt5 import QtCore, QtGui
import sys
from PyQt5.QtCore import QEventLoop, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow

from Ui_ControlBoard import Ui_MainWindow

class EmittingStr(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str) #定义一个发送str的信号
    def write(self, text):
        self.textWritten.emit(str(text))


class ControlBoard(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(ControlBoard, self).__init__()
        self.setupUi(self)
        # 下面将输出重定向到textBrowser中
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)
    def outputWritten(self, text):
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()
    def printABCD(self):
        print("aaaaaaaaaaaaaaaa")
        print("bbbbbbbbbbbbbbbb")
        print("cccccccccccccccc")
        print("dddddddddddddddd")

#有按钮的话，下面的就不要注释掉
    #self.pushButton.clicked.connect(self.bClicked)


'''界面标题，对应界面文件最后注销掉的两行代码。两者选其一撤掉注销
def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "发送端"))
        #self.pushButton.setText(_translate("MainWindow", "PushButton"))
        '''



    
'''这是最常用的格式，如果有按钮的话，下面的就是按钮的功能
def bClicked(self):
    Runs the main function.
    print('Begin')

    self.printABCD()

    print("End")

def printABCD(self):
    print("aaaaaaaaaaaaaaaa")
    print("bbbbbbbbbbbbbbbb")
    print("cccccccccccccccc")
    print("dddddddddddddddd")

'''



#无按钮，下面是自动显示输出的情况







#这里就放自己的输出代码所在的功能代码











if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ControlBoard()
    win.show()
    win.printABCD()
    sys.exit(app.exec_())


