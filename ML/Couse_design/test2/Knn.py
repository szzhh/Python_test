import numpy as np
import matplotlib.pyplot as plt


#树结构类
class Tree(object):
    def __init__(self, cutColumn=None, cutValue=None):
        """
        Parameters
        ----------
        cutColumn : Int, optional
            切分超平面的特征列. The default is None.
        cutValue : float, optional
            切分超平面的特征值. The default is None.
            
        """
        self.cutColumn = cutColumn
        self.cutValue = cutValue
        self.nums = 0                       #个数
        self.rootNums = 0                   #在切分超平面上面的实例个数
        self.leftNums = 0                   #在切分超平面左侧的实例个数
        self.rightNums = 0                  #在切分超平面右侧的实例个数
        self._tree_left = None              #左侧树结构
        self._tree_right = None             #右侧树结构
        self.depth = 0                      #树的深度


#kd树实现KNN算法
class Knn(object):
    def __init__(self, K=1,method='kdtree'):
        self.K_neighbor = K
        self.tree_depth = 0
        self.n_samples = 0
        self.n_features = 0
        self.trainSet = 0
        self.label = 0
        self._tree = 0
        self._method=method
        
    def cal_cutColumn(self, n_iter):
        Co=np.mod(n_iter, self.n_features)
        return Co
    
    def cal_cutValue(self, Xarray):
        if Xarray.__len__() % 2 == 1:
            #单数序列
            cutValue = np.median(Xarray)
        else:
            #双数序列
            cutValue = Xarray[np.argsort(Xarray)[int(Xarray.__len__()/2)]]
        return cutValue    
    
    #造树
    def build_tree(self, X, n_iter=0):
        nums = X.shape[0]
        #不达切分条件，则不生成树，直接返回None
        if nums < 2*self.K_neighbor:
            return None
        #计算切分的列
        cutColumn = self.cal_cutColumn(n_iter)
        Xarray = X[:,cutColumn]
        #计算切分的值
        cutValue = self.cal_cutValue(Xarray)
        #生成当前的树结构
        tree = Tree(cutColumn, cutValue)
        rootIndex = np.nonzero(Xarray==cutValue)[0]
        leftIndex = np.nonzero(Xarray<cutValue)[0]
        rightIndex = np.nonzero(Xarray>cutValue)[0]
        #保存树的结点数量
        tree.nums = nums
        tree.rootNums = len(rootIndex)
        tree.leftNums = len(leftIndex)
        tree.rightNums = len(rightIndex)
        #保存树深，并加1
        tree.depth = n_iter
        n_iter += 1
        #递归添加左侧树枝结构
        X_left = X[leftIndex,:]
        tree._tree_left = self.build_tree(X_left, n_iter)
        #递归添加右侧树枝结构
        X_right = X[rightIndex,:]
        tree._tree_right = self.build_tree(X_right, n_iter)
        return tree
    
    #训练构造kd树
    def train(self, X, y):
        if self._method=='normal':
            self.n_samples, self.n_features = X.shape
            self.trainSet = X
            self.label = y
            self._tree = self.build_tree(X)
            return
        elif self._method=='kdtree':
            self.n_samples, self.n_features = X.shape
            self.trainSet = X
            self.label = y
            return

    #计算欧氏距离
    def caldist(self, X, xi):
        return np.linalg.norm((X-xi), axis=1)    
    
    #计算一堆数据集距离目标点的距离，并返回K个最近值
    def calKneighbor(self, XIndex, xi):
        trainSet = self.trainSet[XIndex,:]
        knnDict = {}
        distArr = self.caldist(trainSet, xi)
        neighborIndex = XIndex[np.argsort(distArr)[:self.K_neighbor]]
        neighborDist = distArr[np.argsort(distArr)[:self.K_neighbor]]
        for i, j in zip(neighborIndex, neighborDist):
            knnDict[i] = j
        return knnDict
    
    #递归搜索树
    def search_tree(self, trainSetIndex, tree, xi):
        trainSet = self.trainSet[trainSetIndex,:]
        #搜索树找到子结点的过程
        if not (tree._tree_left or tree._tree_right):
            self.neighbor = self.calKneighbor(trainSetIndex, xi)
            return
        else:
            cutColumn = tree.cutColumn
            cutValue = tree.cutValue
            #切分平面左边的实例
            chidlLeftIndex = trainSetIndex[np.nonzero(trainSet[:,cutColumn]<cutValue)[0]]
            #切分平面上的实例
            rootIndex = trainSetIndex[np.nonzero(trainSet[:,cutColumn]==cutValue)[0]]
            #切分平面右边的实例
            chidlRightIndex = trainSetIndex[np.nonzero(trainSet[:,cutColumn]>cutValue)[0]]
            #print(tree._tree_left)
            #print(tree._tree_right)
            if tree._tree_left:# and xi[cutColumn] <= cutValue:
                #print('left')
                self.search_tree(chidlLeftIndex, tree._tree_left, xi)
                #回退父结点的过程
                #判断目标点到该切分平面的的距离，计算是否相交
                length = abs(tree.cutValue - xi[cutColumn])
                #不相交的话，则继续回退
                if length >= max(self.neighbor.values()):
                    return
                #相交的话，先是计算分类平面上实例点的距离，再计算另外半边的实例点的距离
                else:
                    targetIndex = list(rootIndex) + list(chidlRightIndex) + list(self.neighbor.keys())
                    self.neighbor = self.calKneighbor(np.array(targetIndex), xi)
                    return
            else:
                self.search_tree(chidlRightIndex, tree._tree_right, xi)
                #回退父结点进行判断
                length = abs(tree.cutValue - xi[cutColumn])
                if length >= max(self.neighbor.values()):
                    return
                else:
                    targetIndex = list(rootIndex) + list(chidlLeftIndex) + list(self.neighbor.keys())
                    self.neighbor = self.calKneighbor(np.array(targetIndex), xi)
                    return

    #搜索kd树
    def predict(self, Xi):
        if self._method=='normal':
            samples, features = Xi.shape
            yp=[]
            for i in range(samples):
                self.neighbor = dict()
                self.search_tree(np.arange(self.n_samples), self._tree, Xi[i,:])
                a=0
                b=0
                for n in self.neighbor.keys():
                    if self.label[n]==0:
                        a+=1
                    if self.label[n]==1:
                        b+=1
                if a>b:
                    yp.append(0)
                else:
                    yp.append(1)
            yp=np.array(yp)
            return yp
        elif self._method=='kdtree':
            samples, features = Xi.shape
            yp=[]
            for i in range(samples):
                self.neighbor = dict()
                self.neighbor = self.calKneighbor(np.arange(self.n_samples), Xi[i,:])
                a=0
                b=0
                for n in self.neighbor.keys():
                    if self.label[n]==0:
                        a+=1
                    if self.label[n]==1:
                        b+=1
                if a>b:
                    yp.append(0)
                else:
                    yp.append(1)
            yp=np.array(yp)
            return yp