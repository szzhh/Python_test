import os
import sys
import time
from threading import Timer
import random
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader

E1=[]#运行进程
E2=[]#就绪队列
E3=[]#后备队列
E4=[]#挂起队列
E5=[]#完成队列
runtime=0 #总时间
n=0
class PCB():
    def __init__(self):
        self.pid = ''     # 进程名称
        self.time=0    # 需要时间片长度
        self.priorty=0     #进程的优先级
        self.state=0     # 进程运行状态，0表示就绪，1表示运行，2表示挂起，-1表示完成  -2表示在后备队列 
        self.property=0  #进程的属性，0表示独立进程，1表示同步进程
        self.memory=0
    
class Mainwindow(QWidget):
    def __init__(self):
        super().__init__()
        qfile_stats=QFile(os.path.split(os.path.realpath(__file__))[0]+'/mainwindow.ui')
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()
        self.ui=QUiLoader().load(qfile_stats)
        canvas = QtGui.QPixmap(211, 1041)
        canvas.fill(QColor("lightgreen"))
        self.ui.label_4.setPixmap(canvas)#创建canvas，并加入label作为画板。
        self.draw(50,200)#绘图函数
        self.pushButton_down = False
        self.ui.pushButton.clicked.connect(self.onButtonClick)
        self.ui.pushButton_2.clicked.connect(self.add)
        self.ui.pushButton_3.clicked.connect(self.ui.close)
        self.ui.pushButton_4.clicked.connect(self.create)

    def create(self):
        global E1
        global E2
        global E3
        global E4
        global E5
        global runtime
        global n
        E1=[]#运行进程
        E2=[]#就绪队列
        E3=[]#后备队列
        E4=[]#挂起队列
        E5=[]#完成队列
        runtime=0 #总时间
        n=0
        num=self.ui.lineEdit_3.text()
        num=eval(num)
        s='初始作业数为：'+str(num)
        self.ui.out.append(s)
        self.ui.out.append('随机产生作业：')
        for i in range(num):
            pcb=PCB()
            pcb.pid='Process_'+str(i+1)
            pcb.time=random.randint(1,10)
            pcb.priorty=random.randint(1,20)
            pcb.state=-2
            pcb.property=0
            pcb.memory=random.randint(5,20)*10
            E3.append(pcb)
            p='PID：'+pcb.pid+'   时间片：'+str(pcb.time)+'   优先级：'+str(pcb.priorty)+'   状态：'+str(pcb.state)+'   属性：'+str(pcb.property)+'   大小：'+str(pcb.memory)
            self.ui.out.append(p)
            self.ui.out.moveCursor(QTextCursor.End)
        #E3.sort(key=lambda x: x.memory,reverse=True)
        self.fill3(E3)
        self.ui.out.append('作业创建成功!')
        self.ui.out.moveCursor(QTextCursor.End)
    def onButtonClick(self):
        global E1
        global E2
        global E3
        global E4
        global E5
        global runtime
        global n
        n+=1
        if n==1:
            E2,E3=self.job_scheduling(E3)
        while len(E2)!=0:
            self.ui.pushButton.setDown(not self.pushButton_down)
            self.pushButton_down=not self.pushButton_down
            runtime+=1
            s1='第'+str(runtime)+'个时间片开始执行'
            s2='第'+str(runtime)+'个时间片执行完毕'
            self.ui.out.append(s1)
            #self.ui.out.repaint()
            self.ui.out.moveCursor(QTextCursor.End)
            #主体内容
            E2.sort(key=lambda x: x.priorty,reverse=True)
            runningPCB=E2.pop(0)#队头进程结点出队
            runningPCB.state=1#队头进程进入运行态
            runningPCB.time-=1#时间片减一
            runningPCB.priorty-=1#优先级减一
            self.ui.E1.setText(runningPCB.pid)
            self.filltable(runningPCB)
            self.fill2(E2)
            time.sleep(0.2)
            #self.clear()
            self.ui.out.append(s2)
            #self.ui.out.repaint()
            self.ui.out.moveCursor(QTextCursor.End)
            if runningPCB.time>0:#仍需要的时间片长度大于0，进程未运行完毕，需重新进入队列
                runningPCB.state=0#队头进程进入就绪态
                E2.append(runningPCB)
            else:
                runningPCB.state=-1
                s4='进程'+runningPCB.pid+'执行完毕！'
                self.ui.out.append(s4)
                self.ui.out.moveCursor(QTextCursor.End)
                E5.append(runningPCB)
                self.fill5(E5)
            self.ui.repaint()
        self.clear()
        self.ui.out.append('所有进程执行完毕！')
        s3='总共执行了'+str(runtime)+'个时间片'
        self.ui.out.append(s3)
        self.ui.out.moveCursor(QTextCursor.End)
        self.ui.pushButton.setChecked(False)
        self.pushButton_down=not self.pushButton_down
    # def run(self):
    #     global E1
    #     global E2
    #     global E3
    #     global E4
    #     global E5
    #     global runtime
    #     #
    #     #if self.pushButton_down==True:
    #     runtime+=1
    #     s1='第'+str(runtime)+'个时间片开始执行'
    #     s2='第'+str(runtime)+'个时间片执行完毕'
    #     self.ui.out.append(s1)
    #     self.ui.out.moveCursor(QTextCursor.End)
    #     #主体内容
    #     E2.sort(key=lambda x: x.priorty,reverse=True)
    #     runningPCB=E2.pop(0)#队头进程结点出队
    #     runningPCB.state=1#队头进程进入运行态
    #     runningPCB.time-=1#时间片减一
    #     runningPCB.priorty-=1#优先级减一
    #     self.ui.E1.setText(runningPCB.pid)
    #     self.filltable(runningPCB)
    #     self.fill2(E2)
    #     time.sleep(4)
    #     #self.clear()
    #     self.ui.out.append(s2)
    #     self.ui.out.moveCursor(QTextCursor.End)
    #     if runningPCB.time>0:#仍需要的时间片长度大于0，进程未运行完毕，需重新进入队列
    #         runningPCB.state=0#队头进程进入就绪态
    #         E2.append(runningPCB)
    #     else:
    #         runningPCB.state=-1
    #         s4='进程'+runningPCB.pid+'执行完毕！'
    #         self.ui.out.append(s4)
    #         self.ui.out.moveCursor(QTextCursor.End)
    #         E5.append(runningPCB)
    #         self.fill5(E5)
            #     if len(E2)==0 and len(E3)==0:
            #         self.ui.out.append('所有进程执行完毕！')
            #         s3='总共执行了'+str(runtime)+'个时间片'
            #         self.ui.out.append(s3)
            #         self.ui.out.moveCursor(QTextCursor.End)
            #         self.ui.pushButton.setChecked(False)
            #         self.pushButton_down=not self.pushButton_down
            #         t.cancel()
            # #多线程
            # t.start()
    def add(self):
        global flag
        flag=False
        self.ui.out.append('进程添加成功')
        self.ui.out.moveCursor(QTextCursor.End)
    def draw(self,y,h):
        painter =QPainter(self.ui.label_4.pixmap())
        brush=QBrush()#添加画笔
        brush.setColor(QColor("blue"))
        brush.setStyle(Qt.SolidPattern)#纯色背景
        painter.setPen(QPen(QColor("blue"), 1))
        painter.setBrush(brush)
        painter.drawRect(0,y,411,h)#矩形坐标+尺寸
        self.ui.label_4.repaint()
        #painter.drawRect(150,150,50,50)
        painter.end()
    def draw1(self,y,h):
        painter =QPainter(self.ui.label_4.pixmap())
        brush=QBrush()#添加画笔
        brush.setColor(QColor("lightgreen"))
        brush.setStyle(Qt.SolidPattern)#纯色背景
        painter.setPen(QPen(QColor("lightgreen"), 1))
        painter.setBrush(brush)
        painter.drawRect(0,y,411,h)#矩形坐标+尺寸
        self.ui.label_4.repaint()
        #painter.drawRect(150,150,50,50)
        painter.end()
    def job_scheduling(self,E3):  #作业调度
        self.ui.out.append('作业调度')
        self.ui.out.moveCursor(QTextCursor.End)
        E=E3
        E3=[]
        self.fill3(E3)
        for i in range(len(E)):
            E[i].state=0
        return E,E3
    def filltable(self,runningPCB):
        self.ui.tableWidget.item(0,0).setText(runningPCB.pid)
        self.ui.tableWidget.item(0,1).setText(str(runningPCB.time))
        self.ui.tableWidget.item(0,2).setText(str(runningPCB.priorty))
        self.ui.tableWidget.item(0,3).setText(str(runningPCB.state))
        self.ui.tableWidget.item(0,4).setText(str(runningPCB.property))
        self.ui.tableWidget.item(0,5).setText(str(runningPCB.memory))
    def clear(self):
        self.ui.E1.setText('')
        self.ui.tableWidget.item(0,0).setText('')
        self.ui.tableWidget.item(0,1).setText('')
        self.ui.tableWidget.item(0,2).setText('')
        self.ui.tableWidget.item(0,3).setText('')
        self.ui.tableWidget.item(0,4).setText('')
        self.ui.tableWidget.item(0,5).setText('')
    def fill2(self,E2):
        self.ui.E2_1.setText('')
        self.ui.E2_2.setText('')
        self.ui.E2_3.setText('')
        self.ui.E2_4.setText('')
        self.ui.E2_5.setText('')
        self.ui.E2_6.setText('')
        self.ui.E2_7.setText('')
        self.ui.E2_8.setText('')
        self.ui.E2_9.setText('')
        self.ui.E2_10.setText('')
        self.ui.E2_11.setText('')
        self.ui.E2_12.setText('')
        self.ui.E2_13.setText('')
        self.ui.E2_14.setText('')
        self.ui.E2_15.setText('')
        self.ui.E2_16.setText('')
        self.ui.E2_17.setText('')
        self.ui.E2_18.setText('')
        for i in range(len(E2)):
            if i==0:
                self.ui.E2_1.setText(E2[i].pid)
            elif i==1:
                self.ui.E2_2.setText(E2[i].pid)
            elif i==2:
                self.ui.E2_3.setText(E2[i].pid)
            elif i==3:
                self.ui.E2_4.setText(E2[i].pid)
            elif i==4:
                self.ui.E2_5.setText(E2[i].pid)
            elif i==5:
                self.ui.E2_6.setText(E2[i].pid)
            elif i==6:
                self.ui.E2_7.setText(E2[i].pid)
            elif i==7:
                self.ui.E2_8.setText(E2[i].pid)
            elif i==8:
                self.ui.E2_9.setText(E2[i].pid)
            elif i==9:
                self.ui.E2_10.setText(E2[i].pid)
            elif i==10:
                self.ui.E2_11.setText(E2[i].pid)
            elif i==11:
                self.ui.E2_12.setText(E2[i].pid)
            elif i==12:
                self.ui.E2_13.setText(E2[i].pid)
            elif i==13:
                self.ui.E2_14.setText(E2[i].pid)
            elif i==14:
                self.ui.E2_15.setText(E2[i].pid)
            elif i==15:
                self.ui.E2_16.setText(E2[i].pid)
            elif i==16:
                self.ui.E2_17.setText(E2[i].pid)
            elif i==17:
                self.ui.E2_18.setText(E2[i].pid)
    def fill3(self,E3):
        self.ui.E3_1.setText('')
        self.ui.E3_2.setText('')
        self.ui.E3_3.setText('')
        self.ui.E3_4.setText('')
        self.ui.E3_5.setText('')
        self.ui.E3_6.setText('')
        self.ui.E3_7.setText('')
        self.ui.E3_8.setText('')
        self.ui.E3_9.setText('')
        self.ui.E3_10.setText('')
        self.ui.E3_11.setText('')
        self.ui.E3_12.setText('')
        self.ui.E3_13.setText('')
        self.ui.E3_14.setText('')
        self.ui.E3_15.setText('')
        self.ui.E3_16.setText('')
        self.ui.E3_17.setText('')
        self.ui.E3_18.setText('')
        self.ui.E3_19.setText('')
        self.ui.E3_20.setText('')
        self.ui.E3_21.setText('')
        self.ui.E3_22.setText('')
        self.ui.E3_23.setText('')
        self.ui.E3_24.setText('')
        self.ui.E3_25.setText('')
        self.ui.E3_26.setText('')
        self.ui.E3_27.setText('')
        for i in range(len(E3)):
            if i==0:
                self.ui.E3_1.setText(E3[i].pid)
            elif i==1:
                self.ui.E3_2.setText(E3[i].pid)
            elif i==2:
                self.ui.E3_3.setText(E3[i].pid)
            elif i==3:
                self.ui.E3_4.setText(E3[i].pid)
            elif i==4:
                self.ui.E3_5.setText(E3[i].pid)
            elif i==5:
                self.ui.E3_6.setText(E3[i].pid)
            elif i==6:
                self.ui.E3_7.setText(E3[i].pid)
            elif i==7:
                self.ui.E3_8.setText(E3[i].pid)
            elif i==8:
                self.ui.E3_9.setText(E3[i].pid)
            elif i==9:
                self.ui.E3_10.setText(E3[i].pid)
            elif i==10:
                self.ui.E3_11.setText(E3[i].pid)
            elif i==11:
                self.ui.E3_12.setText(E3[i].pid)
            elif i==12:
                self.ui.E3_13.setText(E3[i].pid)
            elif i==13:
                self.ui.E3_14.setText(E3[i].pid)
            elif i==14:
                self.ui.E3_15.setText(E3[i].pid)
            elif i==15:
                self.ui.E3_16.setText(E3[i].pid)
            elif i==16:
                self.ui.E3_17.setText(E3[i].pid)
            elif i==17:
                self.ui.E3_18.setText(E3[i].pid)
            elif i==18:
                self.ui.E3_19.setText(E3[i].pid)
            elif i==19:
                self.ui.E3_20.setText(E3[i].pid)
            elif i==20:
                self.ui.E3_21.setText(E3[i].pid)
            elif i==21:
                self.ui.E3_22.setText(E3[i].pid)
            elif i==22:
                self.ui.E3_23.setText(E3[i].pid)
            elif i==23:
                self.ui.E3_24.setText(E3[i].pid)
            elif i==24:
                self.ui.E3_25.setText(E3[i].pid)
            elif i==25:
                self.ui.E3_26.setText(E3[i].pid)
            elif i==26:
                self.ui.E3_27.setText(E3[i].pid)
    def fill5(self,E5):
        self.ui.E5_1.setText('')
        self.ui.E5_2.setText('')
        self.ui.E5_3.setText('')
        self.ui.E5_4.setText('')
        self.ui.E5_5.setText('')
        self.ui.E5_6.setText('')
        self.ui.E5_7.setText('')
        self.ui.E5_8.setText('')
        self.ui.E5_9.setText('')
        self.ui.E5_10.setText('')
        self.ui.E5_11.setText('')
        self.ui.E5_12.setText('')
        self.ui.E5_13.setText('')
        self.ui.E5_14.setText('')
        self.ui.E5_15.setText('')
        self.ui.E5_16.setText('')
        self.ui.E5_17.setText('')
        self.ui.E5_18.setText('')
        self.ui.E5_19.setText('')
        self.ui.E5_20.setText('')
        self.ui.E5_21.setText('')
        self.ui.E5_22.setText('')
        self.ui.E5_23.setText('')
        self.ui.E5_24.setText('')
        self.ui.E5_25.setText('')
        self.ui.E5_26.setText('')
        self.ui.E5_27.setText('')
        for i in range(len(E5)):
            if i==0:
                self.ui.E5_1.setText(E5[i].pid)
            elif i==1:
                self.ui.E5_2.setText(E5[i].pid)
            elif i==2:
                self.ui.E5_3.setText(E5[i].pid)
            elif i==3:
                self.ui.E5_4.setText(E5[i].pid)
            elif i==4:
                self.ui.E5_5.setText(E5[i].pid)
            elif i==5:
                self.ui.E5_6.setText(E5[i].pid)
            elif i==6:
                self.ui.E5_7.setText(E5[i].pid)
            elif i==7:
                self.ui.E5_8.setText(E5[i].pid)
            elif i==8:
                self.ui.E5_9.setText(E5[i].pid)
            elif i==9:
                self.ui.E5_10.setText(E5[i].pid)
            elif i==10:
                self.ui.E5_11.setText(E5[i].pid)
            elif i==11:
                self.ui.E5_12.setText(E5[i].pid)
            elif i==12:
                self.ui.E5_13.setText(E5[i].pid)
            elif i==13:
                self.ui.E5_14.setText(E5[i].pid)
            elif i==14:
                self.ui.E5_15.setText(E5[i].pid)
            elif i==15:
                self.ui.E5_16.setText(E5[i].pid)
            elif i==16:
                self.ui.E5_17.setText(E5[i].pid)
            elif i==17:
                self.ui.E5_18.setText(E5[i].pid)
            elif i==18:
                self.ui.E5_19.setText(E5[i].pid)
            elif i==19:
                self.ui.E5_20.setText(E5[i].pid)
            elif i==20:
                self.ui.E5_21.setText(E5[i].pid)
            elif i==21:
                self.ui.E5_22.setText(E5[i].pid)
            elif i==22:
                self.ui.E5_23.setText(E5[i].pid)
            elif i==23:
                self.ui.E5_24.setText(E5[i].pid)
            elif i==24:
                self.ui.E5_25.setText(E5[i].pid)
            elif i==25:
                self.ui.E5_26.setText(E5[i].pid)
            elif i==26:
                self.ui.E5_27.setText(E5[i].pid)
#类外函数

if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon(os.path.split(os.path.realpath(__file__))[0]+'/logo.png'))
    mainwindow=Mainwindow()
    mainwindow.ui.show()
    app.exec_()
