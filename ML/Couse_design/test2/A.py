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
#-----------------------乳腺癌数据集---------------------------
#读取数据
data = pd.read_csv('breast.csv')
#将B良性替换成0， M恶性替换成1
result = data['diagnosis']
y1 = np.where(result == 'M',1,0)
#删除ID列和标签列
data.drop(['id','diagnosis'],axis=1,inplace=True)
# 提取数据
X1 = data.values.astype(np.float)
#数据标准化
scaler = StandardScaler()
X1 = scaler.fit_transform(X1)
# 特征选择
best = SelectKBest(f_classif, k=20)
X1= best.fit_transform(X1, y1)
features_remain = data.columns.tolist()
index=np.where(best.get_support()==True)[0]
selectname=[features_remain[i] for i in index]
columnsMark1=[1 for i in index]

#-----------------------电信用户流失数据集---------------------------
#读取数据
churn_df = pd.read_csv('churn.csv')
#数据集划分
churn_result = churn_df['Churn?']
y2 = np.where(churn_result == 'True.',1,0)
to_drop = ['State','Area Code','Phone','Churn?']
churn_feat_space = churn_df.drop(to_drop,axis=1)#删除不可用特征
yes_no_cols = ["Int'l Plan","VMail Plan"]
churn_feat_space[yes_no_cols] = churn_feat_space[yes_no_cols] == 'yes'
col_names = churn_feat_space.columns.tolist()
col_lst=[1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1] #1代表连续变量
X2 = churn_feat_space.values.astype(np.float)
#数据标准化
scaler = StandardScaler()
X2 = scaler.fit_transform(X2)
#特征选择
best = SelectKBest(f_classif, k=12)
X2= best.fit_transform(X2, y2)
index=np.where(best.get_support()==True)[0]
columnsMark2=[col_lst[i] for i in index]

#----------------------------------------划分数据集----------------------------------------------
X_train1,X_test1,y_train1,y_test1 = train_test_split(X1,y1,test_size=0.2)
X_train2,X_test2,y_train2,y_test2 = train_test_split(X2,y2,test_size=0.2)

#-----------------------------------------建立模型-----------------------------------------------
print('-----------------------数据集1---------------------------')
y_pred1 = y1.copy()
y_pred2 = y1.copy() 
y_pred3 = y1.copy() 
y_pred4 = y1.copy()
yp1= y1.copy()
yp1.dtype=np.float32
yp2= y2.copy()
yp2.dtype=np.float32
#KNN模型改进前
start=time()
knn=Knn(K=5,method='normal')
knn.train(X_train1,y_train1)
y_pred1= knn.predict(X_test1)
end=time()
print('Knn改进前时间：',end-start)
print('Knn改进前准确率: ',accuracy(y_test1,y_pred1))
print('---------------------------------------------------------')
#KNN模型改进后
start=time()
knn=Knn(K=5,method='kdtree')
knn.train(X_train1,y_train1)
y_pred2= knn.predict(X_test1)
end=time()
print('Knn改进后时间：',end-start)
print('Knn改进后准确率: ',accuracy(y_test1,y_pred2))
print('---------------------------------------------------------')
#BP神经网络模型改进前
start=time()
bp=BPNet(1, [30], 'sigmoid','normal') #输入隐藏层数，隐藏层数量和激活函数
bp.train(X_train1,y_train1,0.1,1000)
y_pred3,yp1 = bp.predict(X_test1)
end=time()
print('BP改进前时间：',end-start)
print('BP改进前准确率: ',accuracy(y_test1,y_pred3))
print('---------------------------------------------------------')
#BP神经网络模型改进后
start=time()
bp=BPNet(1, [30], 'sigmoid','dynamic') #输入隐藏层数，隐藏层数量和激活函数
bp.train(X_train1,y_train1,0.1,1000)
y_pred4,yp2 = bp.predict(X_test1)
end=time()
print('BP改进后时间：',end-start)
print('BP改进后准确率: ',accuracy(y_test1,y_pred4))

#draw_roc1(y_test1,yp1,accuracy(y_test1,y_pred3),y_test1,yp2,accuracy(y_test1,y_pred4),'数据集1BP神经网络改进前后',1)

print()
print('-----------------------数据集2---------------------------')
y_pred1 = y2.copy()
y_pred2 = y2.copy() 
y_pred3 = y2.copy() 
y_pred4 = y2.copy()  
yp1= y1.copy()
yp1.dtype=np.float32
yp2= y2.copy()
yp2.dtype=np.float32

#KNN模型改进前
start=time()
knn=Knn(K=5,method='normal')
knn.train(X_train2,y_train2)
y_pred1= knn.predict(X_test2)
end=time()
print('Knn改进前时间：',end-start)
print('Knn改进前准确率: ',accuracy(y_test2,y_pred1))
print('---------------------------------------------------------')
#KNN模型改进后
start=time()
knn=Knn(K=5,method='kdtree')
knn.train(X_train2,y_train2)
y_pred2= knn.predict(X_test2)
end=time()
print('Knn改进后时间：',end-start)
print('Knn改进后准确率: ',accuracy(y_test2,y_pred2))
print('---------------------------------------------------------')
#BP神经网络模型改进前
start=time()
bp=BPNet(1, [30], 'sigmoid','normal') #输入隐藏层数，隐藏层数量和激活函数
bp.train(X_train2,y_train2,0.1,1000)
y_pred3,yp1 = bp.predict(X_test2)
end=time()
print('BP改进前时间：',end-start)
print('BP改进前准确率: ',accuracy(y_test2,y_pred3))
print('---------------------------------------------------------')
#BP神经网络模型改进后
start=time()
bp=BPNet(1, [30], 'sigmoid','dynamic') #输入隐藏层数，隐藏层数量和激活函数
bp.train(X_train2,y_train2,0.1,1000)
y_pred4,yp2 = bp.predict(X_test2)
end=time()
print('BP改进后时间：',end-start)
print('BP改进后准确率: ',accuracy(y_test2,y_pred4))
#draw_roc1(y_test2,yp1,accuracy(y_test2,y_pred3),y_test2,yp2,accuracy(y_test2,y_pred4),'数据集2BP神经网络改进前后',2)
print()

#plt.show()
