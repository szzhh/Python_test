import numpy as np
import matplotlib.pyplot as plt


class Lr(object):
    """Logistic Regression"""
    def __init__(self):
        self.w = 0                  #系数
        self.b = 0                  #截距
        self.trainSet = 0           #训练集特征
        self.label = 0              #训练集标签
        self.learning_rate = None   #学习率
        self.n_iters = None         #实际迭代次数
        self.accurancy = None       #准确率
        self.tol = 1.0e-5           #停止迭代的容忍度
        self.llList = []            #记录似然值的列表
    
    def train(self, X, y, n_iters=1000, learning_rate=0.01):
        """fit model
        
        Parameters:
        -----------
        X: array-like, 2D shape
            训练集特征
        y: array-like, 1D shape
            训练集标签
        n_iters: Int, default=1000
            优化方法的迭代次数
        learning_rate: float, default=0.01
            学习率，在梯度下降中用得到
        
        results:
        --------
        w: 1D array
            特征的系数
        b: float
            截距
        accurancy: float
            准确率，根据模型优化后自动生成的准确率
        llList: List[float]
            记录每轮迭代的似然值列表
        """
        if X.ndim < 2:
            raise ValueError("X must be 2D array-like!")
        self.trainSet = X
        self.label = y
        self.__train_gradient(n_iters, learning_rate)
        return  
        
    #求p(y=1|x)以及似然值LL
    def PVandLLV(self, X, Y, W):
        """calculate p-value and likelihood-value
        
        Parameters:
        -----------
        X: array, shape=(n_samples, n_features+1)
            特征矩阵，包含了全是1的一列特征
        Y: array, shape=(n_samples, 1)
            标签矩阵
        W: array, shape=(1, n_features+1)
            系数矩阵，包含了截距b
        
        results:
        --------
        p_value: array, shape=(n_samples, 1)
            训练样本的P值
        LL: float
            似然值
        """
        wx = np.dot(X, W.T)
        #为了防止wx过大导致值溢出,统一使大于0的值变成-1，并转换下公式，相当于正值用一个公式，负值用一个公式
        #原式：
        #p_value = np.exp(wx) / (1 + np.exp(wx))
        p_value = np.zeros(wx.shape)
        p_value[wx<0] = np.exp(wx[wx<0]) / (1 + np.exp(wx[wx<0]))
        p_value[wx>=0] = 1 / (1 + np.exp(-1.*wx[wx>=0]))
        #为了防止求解似然函数时溢出，进行公式转变
        #原式：
        ##LLarray = -1.*np.multiply(Y, wx) + np.log(1 + np.exp(wx))
        LLarray = np.zeros(wx.shape)
        LLarray[wx<0] = -1.*np.multiply(Y[wx<0], wx[wx<0]) + np.log(1 + np.exp(wx[wx<0]))
        LLarray[wx>=0] = -1.*np.multiply(Y[wx>=0], wx[wx>=0]) + np.log(1 + np.exp(-1.*wx[wx>=0])) + wx[wx>=0]
        return p_value, LLarray.sum()
    
    #求梯度/一阶导矩阵
    def __calGradient(self, X, Y, Ypre):
        """calculate Gradient Matrix
        
        Parameters:
        -----------
        X: array, shape=(n_samples, n_features+1)
            特征矩阵，包含了全是1的一列特征
        Y: array, shape=(n_samples, 1)
            标签矩阵
        Ypre: array, shape=(n_samples, 1)
            预测的标签P值矩阵

        results:
        --------
        Gw: array, shape=(1, n_features+1)
            梯度矩阵
        """
        Gw = -1.*np.multiply((Y - Ypre), X).sum(axis=0)
        return np.expand_dims(Gw, 0)
    
    #求海塞/二阶导矩阵
    def __calHessian(self, X, Ypre):
        """calculate Hessian Matrix
        
        Parameters:
        -----------
        X: array, shape=(n_samples, n_features+1)
            特征矩阵，包含了全是1的一列特征
        Ypre: array, shape=(n_samples, 1)
            预测的标签P值矩阵

        results:
        --------
        Hw: array, shape=(n_features+1, n_features+1)
            海塞矩阵
        """
        Hw = X.T@(X*Ypre*(1-Ypre))
        return Hw
        
    #训练，梯度下降法
    def __train_gradient(self, n_iters, learning_rate):
        n_samples, n_features = self.trainSet.shape
        X = self.trainSet
        y = self.label
        #合并w和b，在X尾部添加一列全是1的特征
        X2 = np.hstack((X, np.ones((n_samples, 1))))
        #将y转置变为(n_samples,1)的矩阵
        Y = np.expand_dims(y, axis=1)
        #初始化特征系数W
        W = np.zeros((1, n_features+1))
        #初始化似然值，更新前后的似然值之差，训练次数
        Ypreprob, LL0 = self.PVandLLV(X2, Y, W)
        self.llList.append(LL0)
        deltaLL = np.inf
        n = 0
        while (n<n_iters) and (LL0>self.tol) and (abs(deltaLL)>self.tol):
            #计算梯度，更新W
            gra = self.__calGradient(X2, Y, Ypreprob)
            W = W - learning_rate*gra/n_samples
            #计算更新后的误差，并留下来
            Ypreprob, LL1 = self.PVandLLV(X2, Y, W)
            deltaLL = LL0 - LL1
            LL0 = LL1
            self.llList.append(LL0)
            n += 1
        self.n_iters = n
        # self.w = W.flatten()[:-1]
        # self.b = W.flatten()[-1]
        self.w=W
        return

    def predict(self, x_test):
        x_test = np.hstack((x_test, np.ones((x_test.shape[0], 1))))
        wx = np.dot(x_test, self.w.T)
        p_value = np.zeros(wx.shape)
        p_value[wx<0] = np.exp(wx[wx<0]) / (1 + np.exp(wx[wx<0]))
        p_value[wx>=0] = 1 / (1 + np.exp(-1.*wx[wx>=0]))
        Yp = np.argmax(np.column_stack((1-p_value,p_value)), axis=1)
        return Yp,p_value