readyPCBQueue=[]#定义就绪队列
finishPCBQueue=[]#定义完成队列
time=0#使用过的时间片数量

class PCBNode:#进程对象类
    def __init__(self):
        self.name = ''     # 进程名称
        self.RequireTimeSlice=0    # 需要时间片长度
        self.CurrentState=0     # 进程运行状态，0表示就绪，1表示运行，-1表示完成  
        
def input_PCBNode():#定义函数实现进程输入
    pcb=PCBNode()
    pcb.name=input('进程名称:')
    pcb.RequireTimeSlice=input('需要时间片长度:')
    pcb.CurrentState=input('进程运行状态:')
    pcb.RequireTimeSlice=eval(pcb.RequireTimeSlice)
    pcb.CurrentState=eval(pcb.CurrentState)
    readyPCBQueue.append(pcb)
    #return readyPCBQueue
num=input('进程的数量:')
num=eval(num)#定义需要进程的数量，在本程序中我们输入五个进程  str转int
for k in range(num):
    #k=PCBNode()#循环输入num个进程
    input_PCBNode()
while len(readyPCBQueue)!=0:
    runningPCB=PCBNode()#新建队头进程结点
    runningPCB=readyPCBQueue.pop(0)#队头进程结点出队
    PCBNode.CurrentState=1#队头进程进入运行态
    runningPCB.RequireTimeSlice-=1#时间片单位减一
    time+=1#使用过的时间片单位加一
    print("第"+str(time)+"个时间片:"+"进程 " + "<"+str(runningPCB.name)+">" + " 使用了1个CPU时间片,"+str(runningPCB.name)+"需求剩余时间片为：" + str(runningPCB.RequireTimeSlice))
    if runningPCB.RequireTimeSlice>0:#仍需要的时间片长度大于0，进程未运行完毕，需重新进入队列
        runningPCB.CurrentState=0#运行态变为就绪态
        readyPCBQueue.append(runningPCB)#进队操作
        if len(finishPCBQueue)==0:
            print("运行完成的进程为：空")
            print("就绪队列为：")
            for i in range(len(readyPCBQueue)):#打印就绪队列的信息
                print(str(readyPCBQueue[i].name)+"("+str(readyPCBQueue[i].RequireTimeSlice)+"个时间片)")
                if i<(len(readyPCBQueue)-1):
                    print("->")
            print("——————————————————————————————————————————————————————————");
        else:
            print("运行完成的进程为：")
            for j in range(len(finishPCBQueue)):
                print(finishPCBQueue[j].name)#打印在完成队列中的进程名称
            print("就绪队列为：")
            for i in range(len(readyPCBQueue)):#打印就绪队列的信息
                print(str(readyPCBQueue[i].name)+"("+str(readyPCBQueue[i].RequireTimeSlice)+"个时间片)")
                if i<(len(readyPCBQueue)-1):
                    print("->")
            print("——————————————————————————————————————————————————————————")
    else:
        runningPCB.CurrentState = -1#运行态变为完成态
        finishPCBQueue.append(runningPCB)#运行完成的进程进入完成队列
        print(str(runningPCB.name)+"运行完毕")
        print("运行完成的进程为：")
        for j in range(len(finishPCBQueue)):
            print(finishPCBQueue[j].name)#打印在完成队列中的进程名称
        print("就绪队列为：")
        for i in range(len(readyPCBQueue)):#打印就绪队列的信息
            print(str(readyPCBQueue[i].name)+"("+str(readyPCBQueue[i].RequireTimeSlice)+"个时间片)")
            if i<(len(readyPCBQueue)-1):
                print("->")
        if len(readyPCBQueue)>0:
            print("——————————————————————————————————————————————————————————")
if len(readyPCBQueue)==0:#就绪队列为0时输出空值
    print("空")
    print("——————————————————————————————————————————————————————————————")
