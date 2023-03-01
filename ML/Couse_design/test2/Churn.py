import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold
from sklearn.feature_selection import SelectKBest, f_classif
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
churn_df = pd.read_csv('churn.csv')
#解决数据不平衡问题
#churn_df = dataProcess(churn_df)
#数据集划分
churn_result = churn_df['Churn?']
y = np.where(churn_result == 'True.',1,0)
to_drop = ['State','Area Code','Phone','Churn?']
churn_feat_space = churn_df.drop(to_drop,axis=1)#删除不可用特征
yes_no_cols = ["Int'l Plan","VMail Plan"]
churn_feat_space[yes_no_cols] = churn_feat_space[yes_no_cols] == 'yes'
col_names = churn_feat_space.columns.tolist()
col_lst=[1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
X = churn_feat_space.values.astype(np.float)
#数据标准化
scaler = StandardScaler()
X = scaler.fit_transform(X)
#特征选择
best = SelectKBest(f_classif, k=12)
X= best.fit_transform(X, y)
index=np.where(best.get_support()==True)[0]
columnsMark=[col_lst[i] for i in index]

#数据集X、标签y
#-----------------------------------------建立多种模型-----------------------------------------------
kf = KFold(5,shuffle=True) # 5折

#逻辑回归模型
# y_pred1 = y.copy() 
# for train_index, test_index in kf.split(X):
#     X_train, X_test = X[train_index], X[test_index]
#     y_train = y[train_index]
#     lr=Lr()
#     lr.train(X_train,y_train)
#     y_pred1[test_index] = lr.predict(X_test)
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
#     knn=Knn(K=5,method='kdtree')
#     knn.train(X_train,y_train)
#     y_pred4[test_index] = knn.predict(X_test)
# end=time()
# print(end-start)
# print('Knn_accuracy: ',accuracy(y,y_pred4))

#BP神经网络模型
# y_pred5 = y.copy() 
# for train_index, test_index in kf.split(X):
#     X_train, X_test = X[train_index], X[test_index]
#     y_train = y[train_index]
#     bp=BPNet(5, [7,10,15,10,7], 'sigmoid')
#     bp.train(X_train,y_train,0.1,1000)
#     y_pred5[test_index] = bp.predict(X_test)
# print('BPNet_accuracy: ',accuracy(y,y_pred5))