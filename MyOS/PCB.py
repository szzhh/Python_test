class PCB():
    def __init__(self, pid , time,priority,previous,memorysize):
        self.pid = pid
        self.time = time
        self.priority = priority
        self.previous = previous
        self.memorysize = memorysize

    def setpid(self,str):
        self.pid = str

    def __str__(self):
        return (self.pid+","+
        self.time +","+
        self.priority +","+
        self.previous +","+
        self.memorysize )