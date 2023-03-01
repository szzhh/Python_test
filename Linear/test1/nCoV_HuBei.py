import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import csv
dict_data =pd.read_csv('F:\DXYArea.csv',encoding = 'gb2312')
data=np.array(dict_data)
X=[]
time=[]
confirm_Y=[]
list=[]

for i,line in enumerate(data):
    if(line[11]=='武汉'):
    # if (line[2] == '美国'):
        line[18] = line[18][0:-5]
        line[18] = line[18].strip()
        list.append(line)
# 去除重复日期
for j in range(0,len(list)):
    for i in range(0,len(list)-1):
        # print(item[18])
        if(list[i][18]==list[i+1][18]):
            list.pop(i)
            break
for i,line in enumerate(list):
    if(line[11]=='武汉'):
    # if (line[2] == '美国'):
        x=[i]
        y=[line[7]]
        t=[line[18]]
        X.append(x)
        confirm_Y.append(y)
        time.append(t)
X=np.array(X)
confirm_Y=np.array(confirm_Y)
cure_Y=[]
for i,line in enumerate(list):
    if(line[11]=='武汉'):
    # if (line[2] == '美国'):
        y=[line[9]]
        cure_Y.append(y)
cure_Y=np.array(cure_Y)

dead_Y=[]
for i,line in enumerate(list):
    if(line[11]=='武汉'):
    # if (line[2] == '美国'):
        y=[line[10]]
        dead_Y.append(y)
dead_Y=np.array(dead_Y)

poly = PolynomialFeatures(degree=8,include_bias=False)
x_mul = poly.fit_transform(X)
model = LinearRegression()

model.fit(x_mul, confirm_Y)
print(model.coef_)
print(model.intercept_)
print(poly.get_feature_names())
predict_confirm=model.predict(x_mul)
print("回归误差：", np.sqrt(mean_squared_error(confirm_Y, predict_confirm)))

plt.plot(X,predict_confirm)
plt.plot(X,confirm_Y)
plt.show()

poly = PolynomialFeatures(degree=6,include_bias=False)
x_mul = poly.fit_transform(X)
model = LinearRegression()

model.fit(x_mul, cure_Y)
print(model.coef_)
print(model.intercept_)
print(poly.get_feature_names())
predict_cure=model.predict(x_mul)
print("回归误差：", np.sqrt(mean_squared_error(cure_Y, predict_cure)))

plt.plot(X,predict_cure)
plt.plot(X,cure_Y)
plt.show()


model.fit(x_mul, dead_Y)
print(model.coef_)
print(model.intercept_)
print(poly.get_feature_names())
predict_dead=model.predict(x_mul)
print("回归误差：", np.sqrt(mean_squared_error(dead_Y, predict_dead)))

plt.plot(X,predict_dead)
plt.plot(X,dead_Y)
plt.show()

# excelData=[]
# for i in range(len(X)):
#     content=(time[i][0],confirm_Y[i][0],int(predict_confirm[i][0]),cure_Y[i][0],int(predict_cure[i][0]),dead_Y[i][0],int(predict_dead[i][0]))
#     excelData.append(content)

# with open("HuBei.csv", 'w',encoding="utf8",newline='') as f:
#     row = ["时间","真实确诊人数","拟合确诊人数","真实治愈人数","拟合治愈人数","真实死亡","拟合死亡人数"]
#     write = csv.writer(f)
#     write.writerow(row)
#     write.writerows(excelData)
#     print("写入完毕！")