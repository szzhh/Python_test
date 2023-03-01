# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 13:16:42 2020

@author: MS

前面采用决策树桩来进行Bagging集成，效果较差，
现在改用全决策树full-tree来集成，观察效果。
全决策树算法不再自编，直接采用sklearn工具。
"""


import numpy as np
import matplotlib.pyplot as plt
from sklearn import tree

#设置出图显示中文
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def predict(H,X1,X2):
    # 预测结果
    # 仅X1和X2两个特征,X1和X2同维度
    X=np.c_[X1.reshape(-1,1),X2.reshape(-1,1)]
    Y_pre=np.zeros(len(X))
    for h in H:
        Y_pre+=h.predict(X)
    Y_pre=2*(Y_pre>=0)-1
    Y_pre=Y_pre.reshape(X1.shape)
    return Y_pre



#>>>>>西瓜数据集3.0α
X=np.array([[0.697,0.46],[0.774,0.376],[0.634,0.264],[0.608,0.318],[0.556,0.215],
    [0.403,0.237],[0.481,0.149],[0.437,0.211],[0.666,0.091],[0.243,0.267],
    [0.245,0.057],[0.343,0.099],[0.639,0.161],[0.657,0.198],[0.36,0.37],
    [0.593,0.042],[0.719,0.103]])
Y=np.array([1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1])

#>>>>>Bagging
T=20
H=[]       #存储各个决策树桩，每行表示#划分特征,划分点,左枝取值，右枝取值
m=len(Y)
H_pre=np.zeros(m)  #存储每次迭代后H对于训练集的预测结果
error=[]           #存储每次迭代后H的训练误差
for t in range(T):
    boot_strap_sampling=np.random.randint(0,m,m)
    Xbs=X[boot_strap_sampling]
    Ybs=Y[boot_strap_sampling]
    h=tree.DecisionTreeClassifier().fit(Xbs,Ybs)
    H.append(h)
    # 计算并存储当前步的训练误差
    H_pre+=h.predict(X)
    Y_pre=(H_pre>=0)*2-1
    error.append(sum(Y_pre!=Y)/m)


#>>>>>绘制训练误差变化曲线
plt.title('训练误差的变化')
plt.plot(range(1,T+1),error,'o-',markersize=2)
plt.xlabel('基学习器个数')
plt.ylabel('错误率')
plt.show()

#>>>>>观察结果
x1min,x1max=X[:,0].min(),X[:,0].max()
x2min,x2max=X[:,1].min(),X[:,1].max()
x1=np.linspace(x1min-(x1max-x1min)*0.2,x1max+(x1max-x1min)*0.2,100)
x2=np.linspace(x2min-(x2max-x2min)*0.2,x2max+(x2max-x2min)*0.2,100)
X1,X2=np.meshgrid(x1,x2)

for t in [3,5,11]:
    plt.title('前%d个基学习器'%t)
    plt.xlabel('密度')
    plt.ylabel('含糖量')
    # 画样本数据点
    plt.scatter(X[Y==1,0],X[Y==1,1],marker='+',c='r',s=100,label='好瓜')
    plt.scatter(X[Y==-1,0],X[Y==-1,1],marker='_',c='k',s=100,label='坏瓜')
    plt.legend()
    # 画基学习器划分边界
    for i in range(t):
        #由于sklearn.tree类中将决策树的结构参数封装于内部，
        #不方便提取，这里采用一个笨办法：
        #用predict方法对区域内所有数据点(100×100)进行预测，
        #然后再用plt.contour的方法来找出划分边界
        Ypre=predict([H[i]],X1,X2)
        plt.contour(X1,X2,Ypre,colors='k',linewidths=1,levels=[0])
    # 画集成学习器划分边界
    Ypre=predict(H[:t],X1,X2)
    plt.contour(X1,X2,Ypre,colors='r',linewidths=5,levels=[0])
    plt.show()