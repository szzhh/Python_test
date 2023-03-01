import random,math

#进程pcb
class PCB: 
    class table:
        class zt:
            def __init__(self):
                self.knum=None
        def __init__(self,ynum):
            self.lis=[]
            for i in range(ynum):
                self.lis.append(self.zt())
        def myprint(self):
            print('页      块')
            for i in range(len(self.lis)):
                print(i,self.lis[i].knum,end=' ',sep="\t")
                print()
    #FIFO队列
    class que:
        def __init__(self,size):
            self.size=size
            self.lis=[]
        def isempty(self):
            return len(self.lis)
        def isfull(self):
            return len(self.lis)==self.size
        def push(self,num):
            self.lis.append(num)
        def pop(self):
            n=self.lis[0]
            del self.lis[0]
            return n
    def __init__(self,id):
        self.id=id
        self.state='ready'
        self.instruction=[]
        self.waitingtime=0        
        self.next=None
        self.t=self.table(6)
        self.q=self.que(3)

#运行调度队列
class queue:
    def __init__(self):
        self.head=None
        self.tail=None
        self.size=0
    def isempty(self):
        if(self.head):
            return 1
        else:
            return 0
    def insert(self,node):
        node.next=None
        if(self.head==None):
            self.head=node
        else:
            self.tail.next=node
        self.tail=node
        self.size+=1
    def remove(self):
        node=self.head
        self.size-=1
        self.head=self.head.next
        if self.isempty()==0 :
            self.tail=None
        return node

#位示图        
class wst:
    def __init__(self):
        self.lis=[]
        for i in range(64):
            self.lis.append(random.randint(0, 1)) 
    def myprint(self):
        for i in range(64):
            if i%16==15:
                print(self.lis[i])
            else:
                print(self.lis[i],end=',')
    def find(self):
        return self.lis.index(0)

def divide(n):
    return n>>10,n&1023

w=wst()#全局位示图

def run(pid):
    temp=random.randint(0, 6143)
    page,pianyi=divide(temp) 
    if pid.t.lis[page].knum!=None:    
        ss='mingzhong'
    else:
        #queye
        if pid.q.isfull():   #zhihuan
            a=pid.q.pop()
            pid.q.push(page)
            pid.t.lis[page].knum=pid.t.lis[a].knum          
            pid.t.lis[a].knum=None          
        else:
            a=w.find()
            pid.q.push(page)
            pid.t.lis[page].knum=a
            w.lis[a]=1
            
    return temp,hex((pid.t.lis[page].knum<<10)+pianyi)

    
def go():
    readyqueue=queue()
    runningProcess=queue()
    waitingqueue=queue()
    pid0=PCB('PID0')
    pid1=PCB('PID1')
    pid2=PCB('PID2')
    pid3=PCB('PID3') 
    pid4=PCB('PID4') 
    pid0.instruction=['io','cpu','cpu','io','cpu']
    pid1.instruction=['cpu','io','cpu','io']
    pid2.instruction=['io','cpu','cpu','io','io']
    pid3.instruction=['io','io','cpu','io']
    pid4.instruction=['cpu','io','cpu','io'] 
    readyqueue.insert(pid0)
    readyqueue.insert(pid1)
    readyqueue.insert(pid2)
    readyqueue.insert(pid3)
    readyqueue.insert(pid4)
    time=0
    cputime=0
    iotime=0
    
    print('Time   ',pid0.id,'      ',pid1.id,'      ',pid2.id,'      ',pid3.id,'      ',pid4.id,'      ','CPU     IOs')
    
    while readyqueue.isempty() or runningProcess.isempty() or waitingqueue.isempty():
        usecpu=0
        useio=0
        if runningProcess.isempty():
            rh=runningProcess.head
            if len(rh.instruction)==0:
                rh.state='done'
                runningProcess.remove()
        if waitingqueue.isempty():
            wh=waitingqueue.head
            while wh!=None:
                wh.state='waiting'
                wh.waitingtime-=1
                wh=wh.next
            wh=waitingqueue.head
            while wh!=None:
                if wh.waitingtime==-1:
                    if len(wh.instruction):
                        if runningProcess.isempty()==0:
                            runningProcess.insert(waitingqueue.remove())
                        else:
                            readyqueue.insert(waitingqueue.remove())
                    else:
                        wh.state='done'
                        waitingqueue.remove()
                wh=wh.next
        useio=waitingqueue.size
        if readyqueue.isempty():
            reh=readyqueue.head
            while reh!=None :
                reh.state='ready'
                reh=reh.next
        if runningProcess.isempty()==0 and readyqueue.isempty():
            runningProcess.insert(readyqueue.remove())
        if runningProcess.isempty():
            rh=runningProcess.head
            if len(rh.instruction):
                order=rh.instruction[0]
                if order=='cpu' :
                    ljdz,wldz=run(rh)
                    lj=str(ljdz)
                    wl=str(wldz)
                    rh.state='run:cpu '+lj+' '+wl
                    del rh.instruction[0]
                    usecpu+=1
                elif order=='io' :
                    ljdz1,wldz1=run(rh)
                    lj=str(ljdz1)
                    wl=str(wldz1)
                    rh.state='run:io '+lj+' '+wl
                    rh.waitingtime=4
                    del rh.instruction[0]
                    waitingqueue.insert(runningProcess.remove())
                    usecpu+=1
            else:
                rh.state='done'
                runningProcess.remove()
        time+=1
        
        print(time,' ',pid0.state,' ',pid1.state,' ',pid2.state,' ',pid3.state,' ',pid4.state,' ',usecpu,' ',useio,sep='\t')

        if usecpu!=0 :
            cputime+=1
        if useio!=0 :
            iotime+=1
    print('Stats: Total Time ',time)
    print('Stats: CPU Busy ',cputime,' (',cputime/time*100,'% )')
    print('Stats: IO Busy ',iotime,' (',iotime/time*100,'% )')
    print("\n位视图:")
    w.myprint()
    print("\npid0页表:")
    pid0.t.myprint()
    print("\npid1页表:")
    pid1.t.myprint()
    print("\npid2页表:")
    pid2.t.myprint()
    print("\npid3页表:")
    pid3.t.myprint()
    print("\npid4页表:")
    pid4.t.myprint()
    
    
    
if __name__=='__main__':
    go()        
