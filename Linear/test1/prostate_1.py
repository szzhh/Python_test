import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

data= pd.read_csv('C:/Users/szh/Desktop/szh/Python_test/Linear/test1/prostate.csv')

data_1=data[['lcavol', 'lweight', 'age', 'lbph', 'svi', 'lcp', 'gleason', 'pgg45','lpsa']]
sns.heatmap(data_1.corr(),square=True,annot=True,cmap='YlGnBu')
sns.pairplot(data_1,kind='reg',markers='.',size=1)
lst=[]
for i in range(8):
    lst.append(list(data[list(data)[i]]))
nd=np.array(lst)
x=nd.T
y=np.array(list(data.lpsa))
y_1=y.reshape(97,1)
print(pd.DataFrame(np.append(x,y_1,axis=1)).corr())
nums =8
columns = 3
rows = math.ceil(nums / columns)
plt.figure(figsize=(10, 12))
for i in range(nums):
    plt.subplot(rows, columns, i + 1)
    plt.plot(x[:, i], y, "b.", markersize=2)
    plt.title(list(data)[i])
plt.subplots_adjust(hspace=0.8)
plt.show()