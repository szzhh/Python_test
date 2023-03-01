from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from math import sqrt

house = datasets.load_boston()
x = house.data
y = house.target
stand = StandardScaler()
stand_x = stand.fit_transform(x)
best = SelectKBest(f_regression, k=3)
best_x = best.fit_transform(stand_x, y)

train_x, test_x, train_y, test_y = train_test_split(best_x, y, test_size=0.2)
lr = LinearRegression()
lr.fit(train_x, train_y)
predict_y = lr.predict(test_x)
rmse = sqrt(mean_squared_error(test_y, predict_y))
r2 = r2_score(test_y, predict_y)
print("RMSE：", rmse)
print("R_squared：", r2)

plt.figure(figsize=(20,3))
plt.plot(predict_y, "r.--", label="Predict_value")
plt.plot(test_y, "b.-", label="True_value")
plt.legend()
plt.title('Predict-True')
plt.show()



# print(best_x)
# best_index = best.get_support()
# print(stand_x[:, best_index])

