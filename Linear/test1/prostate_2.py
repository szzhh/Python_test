from sklearn import datasets
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from sklearn.model_selection import train_test_split
import sklearn.linear_model
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from math import sqrt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

n=3
data= pd.read_csv('C:/Users/szh/Desktop/szh/Python_test/Linear/test1/prostate.csv')
x=data.drop(['lpsa','train'],axis=1)
y=data['lpsa']
Best=SelectKBest(f_regression, k=n)
bestFeature=Best.fit_transform(x,y)
best=list(x.columns[Best.get_support()])
best.append('lpsa')
best.append('train')
print('BestFeature：',best[0:n])
data=data[best]
#特征归一化
scaler=MinMaxScaler()
for feature in best[0:n+1]:
    data[feature]=scaler.fit_transform(data[[feature]])


'''lst=[]
for i in range(3):
    lst.append(list(data[list(data)[i]]))
nd=np.array(lst)
x=nd.T
y=np.array(list(data.lpsa))
stand = StandardScaler()
stand_x = stand.fit_transform(x)
best = SelectKBest(f_regression, k=1)
best_x = best.fit_transform(stand_x, y)'''

#train_x, test_x, train_y, test_y = train_test_split(best_x, y, test_size=0.5)

data_train=data[data.train=='T']
data_test=data[data.train=='F']
lst=[]
for i in range(n):
    lst.append(list(data_train[list(data_train)[i]]))
nd=np.array(lst)
train_x=nd.T
train_y=np.array(list(data_train.lpsa))
lst=[]
for i in range(n):
    lst.append(list(data_test[list(data_test)[i]]))
nd=np.array(lst)
test_x=nd.T
test_y=np.array(list(data_test.lpsa))
#普通线性回归
#lr = sklearn.linear_model.LinearRegression()
#Lasso回归
#lr = sklearn.linear_model.Lasso()
#岭回归
lr = sklearn.linear_model.Ridge()
#ElasticNet回归
#lr = sklearn.linear_model.ElasticNet()
#多项式回归
# poly = PolynomialFeatures(degree=10,include_bias=False)
# train_x = poly.fit_transform(train_x)
# lr = LinearRegression()
lr.fit(train_x, train_y)
# print(lr.coef_)
# print(lr.intercept_)
# print(poly.get_feature_names())
# print('test_x0')
# print(test_x)
# test_x = poly.fit_transform(test_x)
predict_y = lr.predict(test_x)
rmse = sqrt(mean_squared_error(test_y, predict_y))
r2 = r2_score(test_y, predict_y)
print("RMSE：", rmse)
print("R_squared：", r2)
print('test_x')
print(test_x)
print('test_y')
print(test_y)
print('predict_y')
print(predict_y)

plt.figure(figsize=(8,2))
plt.plot(predict_y, "r.--", label="Predict_value")
plt.plot(test_y, "b.-", label="True_value")
plt.legend()
plt.title("RMSE:"+str(round(rmse,6))+"            R_squared:"+str(round(r2,6)))
plt.ylim(0,2)
plt.show()



# print(best_x)
# best_index = best.get_support()
# print(stand_x[:, best_index])'''

