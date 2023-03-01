import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import *
from Function import  *
from Lr import Lr
from Bayes import Bayes
from Lda import Lda
from Knn import Knn
from BPNet import  BPNet
from time import  *

#-----------------------------------------数据预处理-----------------------------------------------
#读取数据
data = pd.read_csv('breast.csv')
#将B良性替换成0， M恶性替换成1
result = data['diagnosis']
y = np.where(result == 'M',1,0)
#删除ID列和标签列
data.drop(['id','diagnosis'],axis=1,inplace=True)
# 提取数据
X = data.values.astype(np.float)
#数据标准化
scaler = StandardScaler()
X = scaler.fit_transform(X)
# 特征选择
best = SelectKBest(f_classif, k=20)
X= best.fit_transform(X, y)
features_remain = data.columns.tolist()
index=np.where(best.get_support()==True)[0]
selectname=[features_remain[i] for i in index]
columnsMark=[1 for i in index]


#-----------------------------------------建立多种模型-----------------------------------------------
kf = KFold(5,shuffle=True) # 5折

#逻辑回归模型
# y_pred1 = y.copy() 
# for train_index, test_index in kf.split(X):
#     X_train, X_test = X[train_index], X[test_index]
#     y_train = y[train_index]
#     lr=Lr()
#     lr.train(X_train,y_train)
#     y_pred1[test_index]= lr.predict(X_test)
# print('Lr_accuracy: ',accuracy(y,y_pred1))

#朴素贝叶斯模型
# y_pred2 = y.copy() 
# for train_index, test_index in kf.split(X):
#     X_train, X_test = X[train_index], X[test_index]
#     y_train = y[train_index]
#     bs=Bayes()
#     bs.train(X_train,y_train,columnsMark)
#     y_pred2[test_index] = bs.predict(X_test)
# print('Bayes_accuracy: ',accuracy(y,y_pred2))

#线性判别分析模型
y_pred3 = y.copy() 
for train_index, test_index in kf.split(X):
    X_train, X_test = X[train_index], X[test_index]
    y_train = y[train_index]
    lda=Lda()
    lda.train(X_train,y_train)
    y_pred3[test_index] = lda.predict(X_test)
print('Lda_accuracy: ',accuracy(y,y_pred3))

#KNN模型
# start=time()
# y_pred4 = y.copy() 
# for train_index, test_index in kf.split(X):
#     X_train, X_test = X[train_index], X[test_index]
#     y_train = y[train_index]
#     knn=Knn(K=5,method='normal')
#     knn.train(X_train,y_train)
#     y_pred4[test_index] = knn.predict(X_test)
# end=time()
# print(end-start)
# print('Knn_accuracy: ',accuracy(y,y_pred4))

#BP神经网络模型
# y_pred5 = y.copy() 
# yp5 = y.copy()
# yp5.dtype=np.float32
# for train_index, test_index in kf.split(X):
#     X_train, X_test = X[train_index], X[test_index]
#     y_train = y[train_index]
#     bp=BPNet(1, [30], 'sigmoid','dynamic') #输入隐藏层数，隐藏层数量和激活函数
#     #bp=BPNet(5, [20,30,40,30,20], 'sigmoid')
#     bp.train(X_train,y_train,0.1,1000)
#     y_pred5[test_index], yp5[test_index] = bp.predict(X_test)
# print('BPNet_accuracy: ',accuracy(y,y_pred5))
# #输出查准率，查全率，F1，预测的各类别样本数
# print(classification_report(y, y_pred5))
# #绘制ROC曲线并计算AUC
# draw_roc(y,yp5)
