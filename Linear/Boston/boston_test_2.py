from sklearn import datasets
import math
import matplotlib.pyplot as plt
house = datasets.load_boston()
x = house.data
y = house.target
nums = len(house.feature_names)
columns = 3
rows = math.ceil(nums / columns)
plt.figure(figsize=(10, 12))
for i in range(nums):
    plt.subplot(rows, columns, i + 1)
    plt.plot(x[:, i], y, "b.", markersize=2)
    plt.title(house.feature_names[i])
plt.subplots_adjust(hspace=0.8)
plt.show()