import os
import sys
import time
from threading import Thread,Timer
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
E6=[]#阻塞队列
M1=[]#未分分区表
M2=[]#已分分区表
runtime=0 #总时间
pausetime=0.3#暂停时间
n=0
nn=0
class PCB():
    def __init__(self):
        self.pid = ''     # 进程名称
        self.time=0    # 需要时间片长度
        self.priorty=0     #进程的优先级
        self.state=0     # 进程运行状态，0表示就绪，1表示运行，2表示挂起，3表示阻塞，-1表示完成  -2表示在后备队列 
        self.property=0  #进程的属性，0表示独立进程，1表示同步进程
        self.memory=0 #进程的内存大小

class Memorylist():
    def __init__(self):
        self.name = ''
        self.start = 0
        self.length=0       
        self.m_state=0  #0表示未分，1表示已分   
memorylist1=Memorylist()
memorylist1.length=900
M1.append(memorylist1)
# 自定义信号源对象类型
class MySignals(QObject):
    # 定义一种信号，两个参数 类型分别是： QTextBrowser 和 字符串
    # 调用 emit方法 发信号时，传入参数 必须是这里指定的 参数类型
    text_print = Signal(QTextBrowser,str)
    draww1 = Signal(str,str)
    draww2 = Signal(str,str,str)
class Subwindow1(QWidget):
    def __init__(self):
        super().__init__()
        qfile_stats=QFile(os.path.split(os.path.realpath(__file__))[0]+'/subwindow1.ui')
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()
        self.ui=QUiLoader().load(qfile_stats)
        self.ui.pushButton.clicked.connect(self.gettext)
        self.ui.pushButton.clicked.connect(self.ui.close)
    def gettext(self):
        global pcb1
        pcb1=PCB()
        pcb1.pid=self.ui.lineEdit.text()
        pcb1.time=eval(self.ui.lineEdit_2.text())
        pcb1.priorty=eval(self.ui.lineEdit_3.text())
        pcb1.state=eval(self.ui.lineEdit_4.text())
        pcb1.property=eval(self.ui.lineEdit_5.text())
        pcb1.memory=eval(self.ui.lineEdit_6.text())
class Subwindow2(QWidget):
    def __init__(self):
        super().__init__()
        qfile_stats=QFile(os.path.split(os.path.realpath(__file__))[0]+'/subwindow2.ui')
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()
        self.ui=QUiLoader().load(qfile_stats)
        self.ui.pushButton.clicked.connect(self.ui.close)
        self.ui.pushButton_2.clicked.connect(self.ui.close)
        self.ui.pushButton.clicked.connect(self.h1)
        self.ui.pushButton_2.clicked.connect(self.h2)
    def h1(self):  #挂起
        global E2
        global E3
        global E4
        global E5
        global E6
        global nn
        nn=0
        lst2=[]
        lst3=[]
        lst4=[]
        lst5=[]
        lst6=[]
        for i in range(len(E2)):
            lst2.append(E2[i].pid)
        for i in range(len(E3)):
            lst3.append(E3[i].pid)
        for i in range(len(E4)):
            lst4.append(E4[i].pid)
        for i in range(len(E5)):
            lst5.append(E5[i].pid)
        for i in range(len(E6)):
            lst6.append(E6[i].pid)
        h_pid=self.ui.lineEdit.text()
        if h_pid in lst2:
            for i in range(len(E2)):
                if h_pid==E2[i].pid:
                    E4.append(E2.pop(i))
                    E4[-1].state=2
                    break
        elif h_pid in lst3:
            for i in range(len(E3)):
                if h_pid==E3[i].pid:
                    E4.append(E3.pop(i))
                    E4[-1].state=2
                    break
        elif h_pid in lst6:
            for i in range(len(E6)):
                if h_pid==E6[i].pid:
                    E4.append(E6.pop(i))
                    E4[-1].state=2
                    break
        elif h_pid in lst4:
            nn=1
        elif h_pid in lst5:
            nn=2
    def h2(self):  #解挂
        global E3
        global E4
        global E6
        global nn
        nn=0
        lst4=[]
        for i in range(len(E4)):
            lst4.append(E4[i].pid)
        h_pid=self.ui.lineEdit.text()
        if h_pid in lst4:
            for i in range(len(E4)):
                if h_pid==E4[i].pid:
                    E6.append(E4.pop(i))
                    #E6[-1].state=2
                    break
        else:
            nn=1
class Mainwindow(QWidget):
    def __init__(self):
        super().__init__()
        qfile_stats=QFile(os.path.split(os.path.realpath(__file__))[0]+'/mainwindow.ui')
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()
        self.ui=QUiLoader().load(qfile_stats)
        self.ms=MySignals()
        canvas = QtGui.QPixmap(211, 1041)
        canvas.fill(QColor("lightgreen"))
        self.ui.label_4.setPixmap(canvas)#创建canvas，并加入label作为画板。
        #self.draw(50,200)#绘图函数
        self.down=False
        self.ms.text_print.connect(self.printToGui)
        self.ms.draww1.connect(self.d1)
        self.ms.draww2.connect(self.d2)
        self.ui.pushButton.clicked.connect(self.onButtonClick)
        #self.ui.pushButton_2.clicked.connect(self.onButtonClick)
        self.ui.pushButton_5.clicked.connect(self.onButtonClick)
        self.ui.pushButton_3.clicked.connect(self.ui.close)
        self.ui.pushButton_4.clicked.connect(self.create)
    def hh1(self):
        global E2
        global E3
        global E4
        global E6
        global M1
        global M2
        global nn
        if nn==0:
            for i in range(len(M2)):
                if E4[-1].pid==M2[i].name:
                    tran=M2.pop(i)
                    tran.m_state=0
                    M1.append(tran)
                    break
            M1.sort(key=lambda x: x.start,reverse=False)
            M1=self.combine_memory(M1)
            self.drawmemory()
            E2,E3=self.job_scheduling(E2,E3)
            self.fill2(E2)
            self.fill3(E3)
            self.fill4(E4)
            self.fill6(E6)
            sss=E4[-1].pid+'挂起成功！'
            self.ui.out.append(sss)
            self.ui.out.moveCursor(QTextCursor.End)
        elif nn==1:
            self.ui.out.append('Error：该进程已在挂起队列！')
            self.ui.out.moveCursor(QTextCursor.End)
        elif nn==2:
            print('hello')
            self.ui.out.append('Error：该进程已经完成！')
            self.ui.out.moveCursor(QTextCursor.End)
    def hh2(self):
        global E3
        global E4
        global E6
        global nn
        if nn==0:
            self.fill3(E3)
            self.fill4(E4)
            self.fill6(E6)
            sss=E6[-1].pid+'解挂成功！'
            self.ui.out.append(sss)
            self.ui.out.moveCursor(QTextCursor.End)
        elif nn==1:
            self.ui.out.append('挂起队列中无该进程！')
            self.ui.out.moveCursor(QTextCursor.End)
    def puttext(self):
        global pcb1
        global E3
        if pcb1.pid !='':
            E3.append(pcb1)
            self.fill3(E3)
            # global E2
            # E2.append(pcb1)
            # E2.sort(key=lambda x: x.priorty,reverse=True)
            # self.fill2(E2)
            ss=pcb1.pid+'进程添加成功'
            self.ui.out.append(ss)
            self.ui.out.moveCursor(QTextCursor.End)
    def printToGui(self,fb,text):
        fb.append(str(text))
        fb.moveCursor(QTextCursor.End)
        fb.ensureCursorVisible()
    def d1(self,y,h):
        self.draw1(int(y),int(h))
    def d2(self,message,y,h):
        self.draw(int(y),int(h),message)
    def create(self):
        global E1
        global E2
        global E3
        global E4
        global E5
        global E6
        global M1
        global M2
        global runtime
        global n
        E1=[]#运行进程
        E2=[]#就绪队列
        E3=[]#后备队列
        E4=[]#挂起队列
        E5=[]#完成队列
        E6=[]#阻塞队列
        M1=[]#未分分区
        M2=[]#已分分区
        memorylist1=Memorylist()
        memorylist1.length=900
        M1.append(memorylist1)
        self.drawmemory()
        self.fill2(E2)
        self.fill5(E5)
        self.fill6(E6)
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
            pcb.state=-2
            #pcb.property=0
            if i>1 and num>3 and random.random()<0.2:
                pcb.property=random.randint(1,i)
            else:
                pcb.property=0
            #pcb.memory=random.randint(5,15)*10
            pcb.memory=random.randint(50,150)
            if pcb.property==0:
                pcb.priorty=random.randint(1,20)
            elif pcb.property!=0:
                pcb.priorty=E3[pcb.property-1].priorty-5
            E3.append(pcb)
            p='PID：'+pcb.pid+'   时间片：'+str(pcb.time)+'   优先级：'+str(pcb.priorty)+'   状态：'+str(pcb.state)+'   属性：'+str(pcb.property)+'   大小：'+str(pcb.memory)
            self.ui.out.append(p)
            self.ui.out.moveCursor(QTextCursor.End)
        #E3.sort(key=lambda x: x.memory,reverse=True)
        self.fill3(E3)
        self.ui.out.append('作业创建成功!')
        self.ui.out.moveCursor(QTextCursor.End)
    def onButtonClick(self):
        global E2
        global E3
        global n
        n+=1
        if n==1:
            E2,E3=self.job_scheduling(E2,E3)
        self.down=not self.down
        self.ui.pushButton.setChecked(self.down)
        
        def run():
            global E1
            global E2
            global E3
            global E4
            global E5
            global E6
            global M1
            global M2
            global runtime
            global pausetime
            while len(E2)!=0 and self.down:
                runtime+=1
                # s1='第'+str(runtime)+'个时间片开始执行'
                # s2='第'+str(runtime)+'个时间片执行完毕'
                s1='第'+str(runtime)+'个时间片：'
                #self.ms.text_print.emit(self.ui.out,s1)
                #抢占式优先权算法
                E2.sort(key=lambda x: x.priorty,reverse=True)
                lst=[]
                for i in range(len(E5)):
                    lst.append(E5[i].pid)
                i=0
                while i < len(E2):
                    ss='Process_'+str(E2[i].property)
                    if E2[i].property==0 or ss in lst:
                        runningPCB=E2.pop(i)#进程结点出队
                        break
                    if E2[i].property!=0 and ss not in lst:
                        E6.append(E2.pop(i))#进程阻塞
                        i-=1
                        for ii in range(len(M2)):
                            if E6[-1].pid==M2[ii].name:
                                tran=M2.pop(ii)
                                tran.m_state=0
                                M1.append(tran)
                                break
                        M1.sort(key=lambda x: x.start,reverse=False)
                        M1=self.combine_memory(M1)
                        self.drawmemory()
                        E2,E3=self.job_scheduling(E2,E3)#从后备队列中调度
                        self.fill6(E6)
                    i+=1
                runningPCB.state=1#队头进程进入运行态
                runningPCB.time-=1#时间片减一
                runningPCB.priorty-=1#优先级减一
                self.ui.E1.setText(runningPCB.pid)
                self.filltable(runningPCB)
                self.fill2(E2)
                time.sleep(pausetime)
                #从阻塞队列进就绪队列
                lst=[]
                for i in range(len(E5)):
                    lst.append(E5[i].pid)
                i=0
                while i<len(E6):
                    ss='Process_'+str(E6[i].property)
                    if ss in lst or ss=='Process_0':
                        for j in range(len(M1)):
                            if E6[i].memory <= M1[j].length:
                                memorylist2=Memorylist()
                                memorylist2.name=E6[i].pid
                                memorylist2.start=M1[j].start
                                memorylist2.length=E6[i].memory
                                memorylist2.m_state=1
                                M2.append(memorylist2)
                                M2.sort(key=lambda x: x.start,reverse=False)
                                M1[j].start=M1[j].start+E6[i].memory
                                M1[j].length=M1[j].length-E6[i].memory
                                M1.sort(key=lambda x: x.start,reverse=False)
                                M1=self.combine_memory(M1)
                                self.drawmemory()
                                E2.append(E6.pop(i))
                                E2.sort(key=lambda x: x.priorty,reverse=True)
                                self.fill2(E2)
                                self.fill6(E6)
                                i-=1
                                break
                    i+=1
                self.clear()
                s2=s1+'执行进程'+runningPCB.pid
                self.ms.text_print.emit(self.ui.out,s2)
                if runningPCB.time>0:#仍需要的时间片长度大于0，进程未运行完毕，需重新进入队列
                    runningPCB.state=0#队头进程进入就绪态
                    E2.append(runningPCB)
                else:
                    runningPCB.state=-1
                    s4='进程'+runningPCB.pid+'执行完毕！'
                    self.ms.text_print.emit(self.ui.out,s4)
                    E5.append(runningPCB)#将进程添加到完成队列
                    self.fill5(E5)
                    #处理内存
                    for i in range(len(M2)):
                        if runningPCB.pid==M2[i].name:
                            tran=M2.pop(i)
                            tran.m_state=0
                            M1.append(tran)
                            break
                    M1.sort(key=lambda x: x.start,reverse=False)
                    M1=self.combine_memory(M1)
                    self.drawmemory()
                    #从阻塞队列进就绪队列
                    lst=[]
                    for i in range(len(E5)):
                        lst.append(E5[i].pid)
                    i=0
                    while i < len(E6):
                        ss='Process_'+str(E6[i].property)
                        if ss in lst or ss=='Process_0':
                            for j in range(len(M1)):
                                if E6[i].memory <= M1[j].length:
                                    memorylist2=Memorylist()
                                    memorylist2.name=E6[i].pid
                                    memorylist2.start=M1[j].start
                                    memorylist2.length=E6[i].memory
                                    memorylist2.m_state=1
                                    M2.append(memorylist2)
                                    M2.sort(key=lambda x: x.start,reverse=False)
                                    M1[j].start=M1[j].start+E6[i].memory
                                    M1[j].length=M1[j].length-E6[i].memory
                                    M1.sort(key=lambda x: x.start,reverse=False)
                                    M1=self.combine_memory(M1)
                                    self.drawmemory()
                                    E2.append(E6.pop(i))
                                    E2.sort(key=lambda x: x.priorty,reverse=True)
                                    self.fill2(E2)
                                    self.fill6(E6)
                                    i-=1
                                    break
                        i+=1
                    E2,E3=self.job_scheduling(E2,E3)#从后备队列中调度
                    if len(E2)==0 and len(E3)==0 and len(E4)==0:
                        self.ms.text_print.emit(self.ui.out,'-----------------------------------')
                        self.ms.text_print.emit(self.ui.out,'所有进程执行完毕！！！')
                        s3='总共执行了'+str(runtime)+'个时间片！！！'
                        self.ms.text_print.emit(self.ui.out,s3)
                        self.ms.text_print.emit(self.ui.out,'-----------------------------------')
                        self.ui.pushButton.setChecked(False)
                        self.down=not self.down
        #多线程                
        T=Thread(target=run)
        T.start()
    def draw(self,y,h,message):
        painter =QPainter(self.ui.label_4.pixmap())
        brush=QBrush()#添加画笔
        brush.setColor(QColor(0, 85, 255))
        brush.setStyle(Qt.SolidPattern)#纯色背景
        #painter.setPen(QPen(QColor("blue"), 1))
        painter.setBrush(brush)
        painter.drawRect(0,y,411,h)#矩形坐标+尺寸
        painter.setPen(QColor("white"))
        painter.setFont(QFont('微软雅黑', 10))
        painter.drawText(60,(y+h/2+10),message)
        self.ui.label_4.repaint()
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
        painter.end()
    def drawmemory(self):
        global M1
        global M2
        for i in range((len(M1))):
            self.ms.draww1.emit(str(M1[i].start),str(M1[i].length))
            #time.sleep(0.1)
        for i in range((len(M2))):
            self.ms.draww2.emit(M2[i].name,str(M2[i].start),str(M2[i].length))
            #time.sleep(0.005)
    def job_scheduling(self,E2,E3):  #作业调度
        global M1
        global M2
        e2=E2
        e3=E3
        i=0
        N=0
        while i < len(e3):
            for j in range(len(M1)):
                if e3[i].memory<=M1[j].length:
                    if N==0:
                        self.ui.out.append('作业调度(后备队列----->就绪队列)')
                        self.ui.out.moveCursor(QTextCursor.End)
                        N=1
                    memorylist2=Memorylist()
                    memorylist2.name=e3[i].pid
                    memorylist2.start=M1[j].start
                    memorylist2.length=e3[i].memory
                    memorylist2.m_state=1
                    M2.append(memorylist2)
                    M2.sort(key=lambda x: x.start,reverse=False)
                    M1[j].start=M1[j].start+e3[i].memory
                    M1[j].length=M1[j].length-e3[i].memory
                    e=e3.pop(i)
                    e.state=0
                    e2.append(e)
                    i-=1
                    break
            i+=1
        
        M1=self.combine_memory(M1)
        e2.sort(key=lambda x: x.priorty,reverse=True)
        self.fill2(e2)
        self.fill3(e3)
        self.drawmemory()
        for i in range(len(e2)):
            e2[i].state=0
        return e2,e3
    def combine_memory(self,M1):
        Mm=[]
        ii=0
        while ii < len(M1):
            if M1[ii].length==0:
                ii+=1
            else:
                st= M1[ii].start
                sum=0
                if ii<len(M1)-1:
                    while M1[ii].start+M1[ii].length==M1[ii+1].start:
                        sum+=M1[ii].length
                        ii+=1
                        if ii==len(M1)-1:
                            break
                sum+=M1[ii].length
                ii+=1
                memorylist1=Memorylist()
                memorylist1.start=st
                memorylist1.length=sum
                Mm.append(memorylist1)
        Mm.sort(key=lambda x: x.start,reverse=False)
        return Mm
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
    def fill4(self,E4):
        self.ui.E4_1.setText('')
        self.ui.E4_2.setText('')
        self.ui.E4_3.setText('')
        self.ui.E4_4.setText('')
        self.ui.E4_5.setText('')
        self.ui.E4_6.setText('')
        self.ui.E4_7.setText('')
        self.ui.E4_8.setText('')
        self.ui.E4_9.setText('')
        for i in range(len(E4)):
            if i==0:
                self.ui.E4_1.setText(E4[i].pid)
            elif i==1:
                self.ui.E4_2.setText(E4[i].pid)
            elif i==2:
                self.ui.E4_3.setText(E4[i].pid)
            elif i==3:
                self.ui.E4_4.setText(E4[i].pid)
            elif i==4:
                self.ui.E4_5.setText(E4[i].pid)
            elif i==5:
                self.ui.E4_6.setText(E4[i].pid)
            elif i==6:
                self.ui.E4_7.setText(E4[i].pid)
            elif i==7:
                self.ui.E4_8.setText(E4[i].pid)
            elif i==8:
                self.ui.E4_9.setText(E4[i].pid)
    def fill6(self,E6):
        self.ui.E6_1.setText('')
        self.ui.E6_2.setText('')
        self.ui.E6_3.setText('')
        self.ui.E6_4.setText('')
        self.ui.E6_5.setText('')
        self.ui.E6_6.setText('')
        self.ui.E6_7.setText('')
        self.ui.E6_8.setText('')
        self.ui.E6_9.setText('')
        for i in range(len(E6)):
            if i==0:
                self.ui.E6_1.setText(E6[i].pid)
            elif i==1:
                self.ui.E6_2.setText(E6[i].pid)
            elif i==2:
                self.ui.E6_3.setText(E6[i].pid)
            elif i==3:
                self.ui.E6_4.setText(E6[i].pid)
            elif i==4:
                self.ui.E6_5.setText(E6[i].pid)
            elif i==5:
                self.ui.E6_6.setText(E6[i].pid)
            elif i==6:
                self.ui.E6_7.setText(E6[i].pid)
            elif i==7:
                self.ui.E6_8.setText(E6[i].pid)
            elif i==8:
                self.ui.E6_9.setText(E6[i].pid)
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
    app.setWindowIcon(QIcon(os.path.split(os.path.realpath(__file__))[0]+'/icon/logo.ico'))
    mainwindow=Mainwindow()
    mainwindow.ui.show()
    subwindow1=Subwindow1()
    subwindow2=Subwindow2()
    mainwindow.ui.pushButton_2.clicked.connect(subwindow1.ui.show)
    subwindow1.ui.pushButton.clicked.connect(mainwindow.puttext)
    #subwindow1.ui.pushButton.clicked.connect(mainwindow.onButtonClick)
    mainwindow.ui.pushButton_5.clicked.connect(subwindow2.ui.show)
    subwindow2.ui.pushButton.clicked.connect(mainwindow.hh1)
    subwindow2.ui.pushButton_2.clicked.connect(mainwindow.hh2)
    subwindow2.ui.pushButton.clicked.connect(mainwindow.onButtonClick)
    subwindow2.ui.pushButton_2.clicked.connect(mainwindow.onButtonClick)
    app.exec_()
