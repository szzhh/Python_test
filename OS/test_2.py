from tkinter import *
import threading
import time
import random
import os
from queue import Queue

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.x1 = 0
        self.x2 = 0
        self.x3 = 0
        self.x4 = 0
        self.r1 = 0
        self.r2 = 0
        self.r3 = 0
        self.r4 = 0
        self.allow_continue1 = True
        self.allow_continue2 = True
        self.allow_continue3 = True
        self.allow_continue4 = True
        self.tag = True
        self.keep = True  # 中止和继续的状态变化
        self.speed1 = random.randint(4, 10)
        self.speed2 = random.randint(4, 10)
        self.speed3 = random.randint(4, 10)
        self.speed4 = random.randint(4, 10)


        self.createWidget()

    def createWidget(self):
        """创建组件"""
        # 进程1
        self.label1 = Label(root, text="进程1", bg="grey", fg="green", font=("华文行楷", 15))
        self.label1.place(relx=0, rely=0.15)
        self.canvas1 = Canvas(root, width=400, height=40, bg="black")
        self.canvas1.place(relx=0, rely=0.2)
        self.canvas1.config(highlightthickness=0)
        self.canvas1.create_oval(0, 0, 40, 40, fill="yellow", tag="oval1")

        # 进程2
        self.label2 = Label(root, text="进程2", bg="grey", fg="green", font=("华文行楷", 15))
        self.label2.place(relx=0, rely=0.3)
        self.canvas2 = Canvas(root, width=400, height=40, bg="black")
        self.canvas2.place(relx=0, rely=0.35)
        self.canvas2.config(highlightthickness=0)
        self.canvas2.create_oval(0, 0, 40, 40, fill="purple", tag="oval2")

        # 进程3
        self.label3 = Label(root, text="进程3", bg="grey", fg="green", font=("华文行楷", 15))
        self.label3.place(relx=0, rely=0.45)
        self.canvas3 = Canvas(root, width=400, height=40, bg="black")
        self.canvas3.place(relx=0, rely=0.5)
        self.canvas3.config(highlightthickness=0)
        self.canvas3.create_oval(0, 0, 40, 40, fill="red", tag="oval3")

        # 进程4
        self.label4 = Label(root, text="进程4", bg="grey", fg="green", font=("华文行楷", 15))
        self.label4.place(relx=0, rely=0.6)
        self.canvas4 = Canvas(root, width=400, height=40, bg="black")
        self.canvas4.place(relx=0, rely=0.65)
        self.canvas4.config(highlightthickness=0)
        self.canvas4.create_oval(0, 0, 40, 40, fill="blue", tag="oval4")

        # 修饰边框
        self.canvas5 = Canvas(root, width=10, height=265, bg="black")
        self.canvas5.place(relx=0.4, rely=0.2)
        self.canvas5.config(highlightthickness=0)

        # 调度框
        self.canvas6 = Canvas(root, width=400, height=40, bg="black")
        self.canvas6.place(relx=0.41, rely=0.425)
        self.canvas6.config(highlightthickness=0)

        # CPU
        self.canvas7 = Canvas(root, width=120, height=120, bg="black")
        self.canvas7.place(relx=0.81, rely=0.345)
        self.canvas7.config(highlightthickness=0)
        self.canvas7.create_text(60, 60, text="CPU", fill="red", font=("宋体", 20))

        # 中止
        self.b_stop = Button(root, text="中止", width=11, height=1, command=self.stop, state="disabled")
        self.b_stop.place(relx=0.1, rely=0.8)

        # 开始
        self.b_start = Button(root, text="开始", width=11, height=1, command=self.start)
        self.b_start.place(relx=0.3, rely=0.8)

        # 复位
        self.b_restart = Button(root, text="复位", width=11, height=1, command=self.restart)
        self.b_restart.place(relx=0.5, rely=0.8)

        # 关闭
        self.b_close = Button(root, text="关闭", width=11, height=1, command=root.destroy)
        self.b_close.place(relx=0.7, rely=0.8)

    # 中止
    def stop(self):
        if not self.keep:
            self.b_stop.config(text="中止")
            if self.allow_continue1:
                thread1.resume()
            if self.allow_continue2:
                thread2.resume()
            if self.allow_continue3:
                thread3.resume()
            if self.allow_continue4:
                thread4.resume()
            self.keep = True
        else:
            self.b_stop.config(text="继续")
            thread1.pause()
            thread2.pause()
            thread3.pause()
            thread4.pause()
            self.keep = False

    # 开始
    def start(self):
        """开始"""
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        self.b_start["state"] = "disabled"
        self.b_stop["state"] = 'normal'

    # 复位
    def restart(self):
        os.execl(sys.executable, sys.executable, *sys.argv)

    # 判断标志位
    def judge(self):
        self.tag = False
        while not self.tag:
            time.sleep(0.1)

    # 根据CPU调度任务重新画圆
    def draw_new(self):
        while q1.qsize() != 0:
            num = q1.get()
            if num == 1:
                self.canvas6.create_oval(q1.qsize() * 40, 0, q1.qsize() * 40 + 40, 40, fill="yellow", tag="oval1")
                self.r1 = q1.qsize() * 40
            elif num == 2:
                self.canvas6.create_oval(q1.qsize() * 40, 0, q1.qsize() * 40 + 40, 40, fill="purple", tag="oval2")
                self.r2 = q1.qsize() * 40
            elif num == 3:
                self.canvas6.create_oval(q1.qsize() * 40, 0, q1.qsize() * 40 + 40, 40, fill="red", tag="oval3")
                self.r3 = q1.qsize() * 40
            elif num == 4:
                self.canvas6.create_oval(q1.qsize() * 40, 0, q1.qsize() * 40 + 40, 40, fill="blue", tag="oval4")
                self.r4 = q1.qsize() * 40

    # 开始CPU调度任务
    def render(self, flag):
        self.canvas1.delete("oval1")
        self.canvas2.delete("oval2")
        self.canvas3.delete("oval3")
        self.canvas4.delete("oval4")
        time.sleep(0.2)
        self.b_stop["state"] = "disabled"
        self.draw_new()  # 根据CPU调度任务重新画圆
        while q2.qsize() != 0:
            num = q2.get()
            if num == 1:
                if flag != num:
                    thread1.resume()
                    self.judge()
            elif num == 2:
                if flag != num:
                    thread2.resume()
                    self.judge()
            elif num == 3:
                if flag != num:
                    thread3.resume()
                    self.judge()
            elif num == 4:
                if flag != num:
                    thread4.resume()
                    self.judge()

# 自定义线程1
class Thread1(threading.Thread):
    def __init__(self):
        super().__init__()
        self.__flag = threading.Event()  # 用于暂停线程的标识 默认为False
        self.__flag.set()  # 设置为True

    def run(self):
        app.canvas1.delete("oval1")
        while app.x1 < 360:
            app.canvas1.create_oval(app.x1, 0, app.x1+40, 40, fill="yellow", tag="oval1")
            app.canvas1.update()
            self.__flag.wait()  # 为True则立即返回 为False时阻塞直到内部的标识位为True后返回
            time.sleep(0.05)
            app.canvas1.delete("oval1")
            app.x1 += app.speed1
        app.canvas1.create_oval(app.x1, 0, app.x1+40, 40, fill="yellow", tag="oval1")
        q1.put(1)
        q2.put(1)
        if q1.qsize() == 4:
            app.render(flag=1)
            self.draw()
        else:
            app.allow_continue1 = False
            self.__flag.clear()
            self.__flag.wait()  # 为True则立即返回 为False时阻塞直到内部的标识位为True后返回
            self.draw()
            app.tag = True

    # 画圆
    def draw(self):
        app.canvas6.delete("oval1")
        while app.r1 <= 360:
            app.canvas6.create_oval(app.r1, 0, app.r1 + 40, 40, fill="yellow", tag="oval1")
            app.canvas6.update()
            time.sleep(0.05)
            app.canvas6.delete("oval1")
            app.r1 += 10

    # 停止线程
    def pause(self):
        self.__flag.clear()  # 设置为False 让线程阻塞

    # 执行线程
    def resume(self):
        self.__flag.set()    # 设置为True 让线程停止阻塞

# 自定义线程2
class Thread2(threading.Thread):
    def __init__(self):
        super().__init__()
        self.__flag = threading.Event()  # 用于暂停线程的标识 默认为False
        self.__flag.set()  # 设置为True

    def run(self):
        app.canvas2.delete("oval2")
        while app.x2 < 360:
            app.canvas2.create_oval(app.x2, 0, app.x2+40, 40, fill="purple", tag="oval2")
            app.canvas2.update()
            self.__flag.wait()  # 为True则立即返回 为False时阻塞直到内部的标识位为True后返回
            time.sleep(0.05)
            app.canvas2.delete("oval2")
            app.x2 += app.speed2
        app.canvas2.create_oval(app.x2, 0, app.x2+40, 40, fill="purple", tag="oval2")
        q1.put(2)
        q2.put(2)
        if q1.qsize() == 4:
            app.render(flag=2)
            self.draw()
        else:
            app.allow_continue2 = False
            self.__flag.clear()
            self.__flag.wait()  # 为True则立即返回 为False时阻塞直到内部的标识位为True后返回
            self.draw()
            app.tag = True

    # 画圆
    def draw(self):
        app.canvas6.delete("oval2")
        while app.r2 <= 360:
            app.canvas6.create_oval(app.r2, 0, app.r2 + 40, 40, fill="purple", tag="oval2")
            app.canvas6.update()
            time.sleep(0.05)
            app.canvas6.delete("oval2")
            app.r2 += 10

    # 停止线程
    def pause(self):
        self.__flag.clear()  # 设置为False 让线程阻塞

    # 执行线程
    def resume(self):
        self.__flag.set()    # 设置为True 让线程停止阻塞

# 自定义线程3
class Thread3(threading.Thread):
    def __init__(self):
        super().__init__()
        self.__flag = threading.Event()  # 用于暂停线程的标识 默认为False
        self.__flag.set()  # 设置为True

    def run(self):
        app.canvas3.delete("oval3")
        while app.x3 < 360:
            app.canvas3.create_oval(app.x3, 0, app.x3+40, 40, fill="red", tag="oval3")
            app.canvas3.update()
            self.__flag.wait()  # 为True则立即返回 为False时阻塞直到内部的标识位为True后返回
            time.sleep(0.05)
            app.canvas3.delete("oval3")
            app.x3 += app.speed3
        app.canvas3.create_oval(app.x3, 0, app.x3+40, 40, fill="red", tag="oval3")
        q1.put(3)
        q2.put(3)
        if q1.qsize() == 4:
            app.render(flag=3)
            self.draw()
        else:
            app.allow_continue3 = False
            self.__flag.clear()
            self.__flag.wait()  # 为True则立即返回 为False时阻塞直到内部的标识位为True后返回
            self.draw()
            app.tag = True

    # 画圆
    def draw(self):
        app.canvas6.delete("oval3")
        while app.r3 <= 360:
            app.canvas6.create_oval(app.r3, 0, app.r3 + 40, 40, fill="red", tag="oval3")
            app.canvas6.update()
            time.sleep(0.05)
            app.canvas6.delete("oval3")
            app.r3 += 10

    # 停止线程
    def pause(self):
        self.__flag.clear()  # 设置为False 让线程阻塞

    # 执行线程
    def resume(self):
        self.__flag.set()    # 设置为True 让线程停止阻塞

# 自定义线程4
class Thread4(threading.Thread):
    def __init__(self):
        super().__init__()
        self.__flag = threading.Event()  # 用于暂停线程的标识 默认为False
        self.__flag.set()  # 设置为True

    def run(self):
        app.canvas4.delete("oval4")
        while app.x4 < 360:
            app.canvas4.create_oval(app.x4, 0, app.x4+40, 40, fill="blue", tag="oval4")
            app.canvas4.update()
            self.__flag.wait()  # 为True则立即返回 为False时阻塞直到内部的标识位为True后返回
            time.sleep(0.05)
            app.canvas4.delete("oval4")
            app.x4 += app.speed4
        app.canvas4.create_oval(app.x4, 0, app.x4+40, 40, fill="blue", tag="oval4")
        q1.put(4)
        q2.put(4)
        if q1.qsize() == 4:
            app.render(flag=4)
            self.draw()
        else:
            app.allow_continue4 = False
            self.__flag.clear()
            self.__flag.wait()  # 为True则立即返回 为False时阻塞直到内部的标识位为True后返回
            self.draw()
            app.tag = True

    # 画圆
    def draw(self):
        app.canvas6.delete("oval4")
        while app.r4 <= 360:
            app.canvas6.create_oval(app.r4, 0, app.r4 + 40, 40, fill="blue", tag="oval4")
            app.canvas6.update()
            time.sleep(0.05)
            app.canvas6.delete("oval4")
            app.r4 += 10

    # 停止线程
    def pause(self):
        self.__flag.clear()  # 设置为False 让线程阻塞

    # 执行线程
    def resume(self):
        self.__flag.set()    # 设置为True 让线程停止阻塞

if __name__ == '__main__':
    root = Tk()
    root.geometry('1000x500+500+200')
    root.title('模拟进程调度')
    root.configure(bg='grey')

    app = Application(master=root)
    q1 = Queue(maxsize=4)
    q2 = Queue(maxsize=4)

    thread1 = Thread1()
    thread2 = Thread2()
    thread3 = Thread3()
    thread4 = Thread4()
    thread1.setDaemon(True)  # 设置线程守护
    thread2.setDaemon(True)  # 设置线程守护
    thread3.setDaemon(True)  # 设置线程守护
    thread4.setDaemon(True)  # 设置线程守护

    root.mainloop()
