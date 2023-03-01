from NaiveBayes import NBayes
#from Semi_NaiveBayes import *
import numpy as np



class Bayes(NBayes):
    #初始化属性，增加
    def __init__(self, algorithm="Naive", solver="Gaussian"):
        """
        贝叶斯的方法类，可选择朴素贝叶斯、半朴素贝叶斯等
        
        Parameters
        ----------
        algorithm : String, optional
            选择的贝叶斯方法，默认是Naive，可选择AODE, TAN
        solver : String, optional
            选择的概率密度函数，默认是Gaussian，可选择

        
        """
        super(Bayes, self).__init__()
        self.algorithm = algorithm
        self.solver = solver
        
    
    #训练参数
    def train(self, X, y, columnsMark):
        self.NaiveTrain(X, y, columnsMark)
    
    
    #预测
    def predict(self, X):
        proba,yp = self.naivepredict(X)
        return proba,yp
    
    
    #取对数预测
    def predictLog(self, X):
        proba_log = self.naivepredictLog(X)
        return proba_log
        
    
    #朴素贝叶斯训练参数
    def NaiveTrain(self, X, y, columnsMark):
        self.n_samples, self.n_features = X.shape
        #计算类别的先验概率
        self.calPy(y)
        #区分特征是离散特征还是连续特征，分别计算条件概率或者均值标准差
        Pxy = {}
        for xIdx in range(self.n_features):
            Xarr = X[:, xIdx]
            #第一层是不同的特征
            if columnsMark[xIdx] == 0:
                #特征是离散
                Pxy[xIdx] = self.categoryTrain(Xarr, y)                                                  
            else:
                #特征是连续
                Pxy[xIdx] = self.continuousTrain(Xarr, y)
        self.xyProba = Pxy
        self.trainSet = X
        self.trainLabel = y
        self.columnsMark = columnsMark
        return

    
    def categoryTrain(self, Xarr, y, LS=True):
        categoryParams = {}
        XiSet = np.unique(Xarr)
        XiSetCount = XiSet.size
        for yi, yiCount in self.ySet.items():
            #第二层是不同的分类标签
            categoryParams[yi] = {}
            Xiyi = Xarr[np.nonzero(y==yi)[0]]
            for xi in XiSet:
                #第三层是变量X的不同值类型
                categoryParams[yi][xi] = self.classifyProba(xi, Xiyi, XiSetCount)    
        return categoryParams
    
    
    def continuousTrain(self, Xarr, y):
        continuousParams = {}
        for yi, yiCount in self.ySet.items():
            #第二层是不同的分类标签
            Xiyi = Xarr[np.nonzero(y==yi)[0]]
            continuousParams[yi] = (Xiyi.mean(), Xiyi.std())
        return continuousParams
    
    
    #连续变量计算概率密度
    def continuousProba(self, x, miu, sigma):
        if self.solver == "Gaussian":
            Pxy = self.gaussianProba(x, miu, sigma)
        else:
            pass
        return Pxy
    
    
    #高斯概率密度
    def gaussianProba(self, x, miu, sigma):
        Pxy = np.exp(-(x-miu)**2/(2*sigma**2))/(np.power(2*np.pi, 0.5)*sigma)
        return Pxy
    
    
    def naivepredict(self, X):
        m, n = X.shape
        proba = np.zeros((m, len(self.yProba)))
        for i in range(m):
            for idx, (yi, Py) in enumerate(self.yProba.items()):
                proba_idx = Py
                for xIdx in range(n):
                    xi = X[i, xIdx]
                    if self.columnsMark[xIdx] == 0:
                        try:
                            proba_idx *= self.xyProba[xIdx][yi][xi]
                        except:
                            pass
                    else:
                        proba_idx *= self.continuousProba(xi, self.xyProba[xIdx][yi][0], self.xyProba[xIdx][yi][1])
                proba[i, idx] = proba_idx
        yPredict = np.argmax(proba, axis=1)
        return yPredict,proba[:,1]


    #防止值溢出，预测时取对数
    def naivepredictLog(self, X):
        m, n = X.shape
        log_proba = np.zeros((m, len(self.yProba)))
        for i in range(m):
            for idx, (yi, Py) in enumerate(self.yProba.items()):
                log_proba_idx = 0
                for xIdx in range(n):
                    xi = X[i, xIdx]
                    if self.columnsMark[xIdx] == 0:
                        log_proba_idx += np.log(self.xyProba[xIdx][yi][xi])
                    else:
                        log_proba_idx += np.log(self.continuousProba(xi, self.xyProba[xIdx][yi][0], self.xyProba[xIdx][yi][1]))
                log_proba[i, idx] = log_proba_idx+np.log(Py)
        return log_proba
    

