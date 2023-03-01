import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold,train_test_split
from sklearn.feature_selection import SelectKBest, f_classif
from Function import  *
from Lr import Lr
from Bayes import Bayes
from Lda import Lda
from Knn import Knn
from BPNet import  BPNet
from time import  *

#-----------------------------------------数据预处理-----------------------------------------------
print('-----------------------数据集2--------------------')
print()
#-----------------------无特征提取---------------------------
#读取数据
df = pd.read_csv('depressed.csv')
#删除有缺失值的行
df.dropna(inplace=True)
#数据集划分
result = df['depressed']
y1 = np.where(result == 1,1,0)
depressed_df =df.drop(['Survey_id','Ville_id','depressed'],axis=1)#删除不可用特征
col_names = depressed_df.columns.tolist()
col_lst=[0,1,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,0,1,1]
X1 = depressed_df.values.astype(np.float)
#数据标准化
scaler = StandardScaler()
X1 = scaler.fit_transform(X1)
columnsMark1=col_lst

#-----------------------有特征提取---------------------------
#读取数据
df = pd.read_csv('depressed.csv')
#删除有缺失值的行
df.dropna(inplace=True)
#数据集划分
result = df['depressed']
y2 = np.where(result == 1,1,0)
depressed_df =df.drop(['Survey_id','Ville_id','depressed'],axis=1)#删除不可用特征
col_names = depressed_df.columns.tolist()
col_lst=[0,1,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,0,1,1]
X2 = depressed_df.values.astype(np.float)
#数据标准化
scaler = StandardScaler()
X2 = scaler.fit_transform(X2)
#特征选择
best = SelectKBest(f_classif, k=18)
X2= best.fit_transform(X2, y2)
index=np.where(best.get_support()==True)[0]
columnsMark2=[col_lst[i] for i in index]

#----------------------------------------划分数据集----------------------------------------------
X_train1,X_test1,y_train1,y_test1 = train_test_split(X1,y1,test_size=0.25)
X_train2,X_test2,y_train2,y_test2 = train_test_split(X2,y2,test_size=0.25)

#-----------------------------------------建立模型-----------------------------------------------
#逻辑回归模型
print('-------------------逻辑回归----------------')
y_pred1 = y1.copy()
yp1= y1.copy()
#yp1.dtype=np.float32
y_pred2 = y2.copy()
yp2 =  y2.copy()
#yp2.dtype=np.float32
lr=Lr()
lr.train(X_train1,y_train1)
y_pred1,yp1= lr.predict(X_test1)
print('Lr无特征提取准确率：',accuracy(y_test1,y_pred1))

lr=Lr()
lr.train(X_train2,y_train2)
y_pred2,yp2= lr.predict(X_test2)
print('Lr有特征提取准确率：',accuracy(y_test2,y_pred2))
print()

draw_roc(y_test1,yp1,accuracy(y_test1,y_pred1),y_test2,yp2,accuracy(y_test2,y_pred2),'逻辑回归',1)

# #朴素贝叶斯模型
# print('------------------朴素贝叶斯---------------')
# y_pred1 = y1.copy()
# yp1= y1.copy()
# y_pred2 = y2.copy()
# yp2 =  y2.copy()
# bs=Bayes()
# bs.train(X_train1,y_train1,columnsMark1)
# y_pred1,yp1= bs.predict(X_test1)
# print('Bayes无特征提取准确率：',accuracy(y_test1,y_pred1))

# bs=Bayes()
# bs.train(X_train2,y_train2,columnsMark2)
# y_pred2,yp2= bs.predict(X_test2)
# print('Bayes有特征提取准确率：',accuracy(y_test2,y_pred2))
# print()

# draw_roc(y_test1,yp1,accuracy(y_test1,y_pred1),y_test2,yp2,accuracy(y_test2,y_pred2),'朴素贝叶斯',2)

# #线性判别分析模型
# print('-----------------线性判别分析--------------')
# y_pred1 = y1.copy()
# yp1= y1.copy()
# y_pred2 = y2.copy()
# yp2 =  y2.copy()
# lda=Lda()
# lda.train(X_train1,y_train1)
# y_pred1,yp1= lda.predict(X_test1)
# print('Lda无特征提取准确率：',accuracy(y_test1,y_pred1))

# lda=Lda()
# lda.train(X_train2,y_train2)
# y_pred2,yp2= lda.predict(X_test2)
# print('Lda有特征提取准确率：',accuracy(y_test2,y_pred2))
# print()

# draw_roc(y_test1,yp1,accuracy(y_test1,y_pred1),y_test2,yp2,accuracy(y_test2,y_pred2),'线性判别分析',3)

# #KNN模型
# print('--------------------K近邻------------------')
# y_pred1 = y1.copy()
# y_pred2 = y2.copy()
# knn=Knn(K=5,method='kdtree')
# knn.train(X_train1,y_train1)
# y_pred1= knn.predict(X_test1)
# print('Knn无特征提取准确率：',accuracy(y_test1,y_pred1))

# knn=Knn(K=5,method='kdtree')
# knn.train(X_train2,y_train2)
# y_pred2= knn.predict(X_test2)
# print('Knn有特征提取准确率：',accuracy(y_test2,y_pred2))
# print()

# #BP神经网络模型
# print('------------------BP神经网络---------------')
# y_pred1 = y1.copy()
# yp1= y1.copy()
# # yp1.dtype=np.float32
# y_pred2 = y2.copy()
# yp2 =  y2.copy()
# # yp2.dtype=np.float32
# bp=BPNet(1, [30], 'sigmoid','dynamic')
# bp.train(X_train1,y_train1,0.1,1000)
# y_pred1,yp1= bp.predict(X_test1)
# print('BP无特征提取准确率：',accuracy(y_test1,y_pred1))

# bp=BPNet(1, [30], 'sigmoid','dynamic')
# bp.train(X_train2,y_train2,0.1,1000)
# y_pred2,yp2= bp.predict(X_test2)
# print('BP有特征提取准确率：',accuracy(y_test2,y_pred2))
# print()

# draw_roc(y_test1,yp1,accuracy(y_test1,y_pred1),y_test2,yp2,accuracy(y_test2,y_pred2),'BP神经网络',4)

plt.show()