# a_star.py

import sys
import time

import numpy as np
class Map:
    def __init__(self,widthNum=10,heightNum=10):
        self.widthNum = widthNum
        self.heightNum=heightNum
        self.obstacle_points =[]
    def IsObstacle(self, i ,j):
        for p in self.obstacle_points:
            if i==p.x and j==p.y:
                return True
        return False

class Point:
    def __init__(self, x, y,beforeCost=0,afterCost=0,totalCost=0):
        self.x = x
        self.y = y
        self.beforeCost=beforeCost
        self.afterCost=afterCost
        self.cost = totalCost

class prioQueue:
    def __init__(self, arithLabel,elist=None, ):
        if elist is None:
            elist = []
        self.open_set = list(elist)
        self.label=arithLabel#label=A,DFS,greed
        if elist:
            self.buildheap()
    def change_mode(self,label):
        self.label=label

    def siftdown(self, e, begin, end):#label=A,DFS,greed
        elems, i, j, = self.open_set, begin, begin * 2 + 1
        while j < end:
            if self.label=='A*':
                if j + 1 < end and elems[j + 1].cost < elems[j].cost:
                    j = j + 1
                if e.cost < elems[j].cost:
                    break
            if self.label=='DFS':
                if j + 1 < end and elems[j + 1].beforeCost < elems[j].beforeCost:
                    j = j + 1
                if e.beforeCost < elems[j].beforeCost:
                    break
            if self.label=='greed':
                if j + 1 < end and elems[j + 1].afterCost < elems[j].afterCost:
                    j = j + 1
                if e.afterCost < elems[j].afterCost:
                    break
            elems[i] = elems[j]
            i, j = j, 2 * j + 1
            elems[i] = e

    def buildheap(self):
        end = len(self.open_set)
        for i in range(end // 2, -1, -1):
            self.siftdown(self.open_set[i], i, end)
        return self.open_set
    def _in(self,point):
        self.open_set.append(point)
        self.buildheap()
    def _out(self):
        self.root=self.open_set[0]
        del self.open_set[0]
        if len(self.open_set)>=1:
            self.buildheap()
        return self.root
class AStar:
    def __init__(self, map,startPoint,endPoint,arithLabel):
        self.map=map
        self.arithLabel="A*"
        self.open_set =prioQueue(arithLabel)
        self.close_set = []
        self.startPoint=startPoint
        self.endPoint=endPoint
        self.path=[]
        self.open_set._in(startPoint)
        self.cost_list = []


    def BaseCost(self, p):
        x_dis = abs(p.x-self.startPoint.x)
        y_dis = abs(p.y-self.startPoint.y)
        # Distance to start point
        return x_dis + y_dis + (np.sqrt(2) - 2) * min(x_dis, y_dis)

    def HeuristicCost(self, p):
        x_dis = abs(self.endPoint.x - p.x)
        y_dis = abs(self.endPoint.y - p.y)
        # Distance to end point
        return x_dis + y_dis + (np.sqrt(2) - 2) * min(x_dis, y_dis)

    def TotalCost(self, p):
        return self.BaseCost(p) + self.HeuristicCost(p)

    def IsValidPoint(self, x, y):
        if x < 0 or y < 0:
            return False
        if x >= self.map.widthNum or y >= self.map.heightNum:
            return False
        return not self.map.IsObstacle(x, y)

    def IsInPointList(self, p, point_list):
        for point in point_list:
            if point.x == p.x and point.y == p.y:
                return True
        return False

    def IsInOpenList(self, p):
        return self.IsInPointList(p, self.open_set.open_set)

    def IsInCloseList(self, p):
        return self.IsInPointList(p, self.close_set)

    def IsStartPoint(self, p):
        return p.x == self.startPoint.x and p.y ==self.startPoint.y

    def IsEndPoint(self, p):
        return p.x == self.endPoint.x and p.y == self.endPoint.y

    def ProcessPoint(self, x, y, parent):
        if not self.IsValidPoint(x, y):
            return # Do nothing for invalid point
        p = Point(x, y)
        p=Point(x,y,self.BaseCost(p),self.HeuristicCost(p),self.TotalCost(p))
        if self.IsInCloseList(p):
            return # Do nothing for visited point
        print('Process Point [', p.x, ',', p.y, ']', ', beforeCost: ', p.beforeCost,', afterCost: ',p.afterCost,', totalCost: ',p.cost)
        if not self.IsInOpenList(p):
            p.parent = parent
            p.cost = self.TotalCost(p)
            p.beforeCost=self.BaseCost(p)
            p.afterCost=self.HeuristicCost(p)
            self.open_set._in(p)

    # def SelectPointInOpenList(self):
    #
    #
    #     index = 0
    #     selected_index = -1
    #     min_cost = sys.maxsize
    #     for p in self.open_set.open_set:
    #         cost = self.TotalCost(p)
    #         if cost < min_cost:
    #             min_cost = cost
    #             selected_index = index
    #         index += 1
    #     return selected_index

    def BuildPath(self, p):
        while True:
            self.path.insert(0, p) # Insert first
            if self.IsStartPoint(p):
                break
            else:
                p = p.parent

        print('===== Algorithm finish ')

    def RunAll(self,):
        while True:

            # if index < 0:
            #     print('No path found, algorithm failed!!!')
            #     return
            p = self.open_set._out()

            if self.IsEndPoint(p):
                return self.BuildPath(p)


            self.close_set.append(p)

            # Process all neighbors
            x = p.x
            y = p.y
            boolList = [True, True, True, True]
            if ((not self.IsValidPoint(x - 1, y)) and (not self.IsValidPoint(x, y + 1))):
                boolList[0] = False
            if ((not self.IsValidPoint(x - 1, y)) and (not self.IsValidPoint(x, y - 1))):
                boolList[1] = False
            if ((not self.IsValidPoint(x, y - 1)) and (not self.IsValidPoint(x + 1, y))):
                boolList[2] = False
            if ((not self.IsValidPoint(x + 1, y)) and (not self.IsValidPoint(x, y + 1))):
                boolList[3] = False
            if (boolList[0]):
                self.ProcessPoint(x - 1, y + 1, p)
            self.ProcessPoint(x - 1, y, p)
            if (boolList[1]):
                self.ProcessPoint(x - 1, y - 1, p)
            self.ProcessPoint(x, y - 1, p)
            if (boolList[2]):
                self.ProcessPoint(x + 1, y - 1, p)
            self.ProcessPoint(x + 1, y, p)
            if (boolList[3]):
                self.ProcessPoint(x + 1, y + 1, p)
            self.ProcessPoint(x, y + 1, p)

    def RunOnce(self,):

        # if index < 0:
        #     print('No path found, algorithm failed!!!')
        #     return
        p = self.open_set._out()
        if self.IsEndPoint(p):
            self.BuildPath(p)
            return self.open_set.open_set, self.close_set, self.path

        self.close_set.append(p)

            # Process all neighbors
        x = p.x
        y = p.y
        boolList=[True,True,True,True]
        if((not self.IsValidPoint(x-1, y))and(not self.IsValidPoint(x, y+1))):
            boolList[0]=False
        if ((not self.IsValidPoint(x - 1, y)) and (not self.IsValidPoint(x, y-1))):
            boolList[1] = False
        if ((not self.IsValidPoint(x, y-1)) and (not self.IsValidPoint(x+1, y))):
            boolList[2] = False
        if ((not self.IsValidPoint(x+1, y)) and (not self.IsValidPoint(x, y+1))):
            boolList[3] = False
        if(boolList[0]):
            self.ProcessPoint(x-1, y+1, p)
        self.ProcessPoint(x-1, y, p)
        if(boolList[1]):
            self.ProcessPoint(x-1, y-1, p)
        self.ProcessPoint(x, y-1, p)
        if (boolList[2]):
            self.ProcessPoint(x+1, y-1, p)
        self.ProcessPoint(x+1, y, p)
        if (boolList[3]):
            self.ProcessPoint(x+1, y+1, p)
        self.ProcessPoint(x, y+1, p)
        return self.open_set.open_set,self.close_set,self.path