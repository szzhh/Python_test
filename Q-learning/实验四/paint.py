# 更改读取的csv文件地址，更改横纵坐标及图例，图片可保存为svg，png等形式。

import seaborn as sns
from matplotlib.font_manager import FontProperties

sns.set_style('whitegrid')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def get_data():
    '''获取数据
    '''
    mod='loss.csv'
    df1 = pd.DataFrame(pd.read_csv('./smooth1/1_90_'+mod, header=0))
    data = np.array(df1).transpose()  # 转置
    cond0 = data[1].reshape((1, 1000))
    cond1 = data[2].reshape((1, 1000))  # 转换成二维数组
    cond_1 = np.vstack((cond0, cond1)).transpose()
    
    df1 = pd.DataFrame(pd.read_csv('./smooth1/1_93_'+mod, header=0))
    data = np.array(df1).transpose()  # 转置
    cond0 = data[1].reshape((1, 1000))
    cond1 = data[2].reshape((1, 1000))  # 转换成二维数组
    cond_2 = np.vstack((cond0, cond1)).transpose()

    df1 = pd.DataFrame(pd.read_csv('./smooth1/1_94_'+mod, header=0))
    data = np.array(df1).transpose()  # 转置
    cond0 = data[1].reshape((1, 1000))
    cond1 = data[2].reshape((1, 1000))  # 转换成二维数组
    cond_3 = np.vstack((cond0, cond1)).transpose()

    df1 = pd.DataFrame(pd.read_csv('./smooth1/1_95_'+mod, header=0))
    data = np.array(df1).transpose()  # 转置
    cond0 = data[1].reshape((1, 1000))
    cond1 = data[2].reshape((1, 1000))  # 转换成二维数组
    cond_4 = np.vstack((cond0, cond1)).transpose()
    
    df1 = pd.DataFrame(pd.read_csv('./smooth1/1_96_'+mod, header=0))
    data = np.array(df1).transpose()  # 转置
    cond0 = data[1].reshape((1, 1000))
    cond1 = data[2].reshape((1, 1000))  # 转换成二维数组
    cond_5 = np.vstack((cond0, cond1)).transpose()
    
    return cond_1, cond_2, cond_3, cond_4, cond_5


data = get_data()
#label = ['lr = 0.5e-3', 'lr = 1e-3', 'lr = 1.5e-3', 'lr = 2e-3', 'lr = 3e-3']
label = ['gamma = 0.90', 'gamma = 0.93', 'gamma = 0.94', 'gamma = 0.95', 'gamma = 0.96']
df = []
for i in range(len(data)):
    df.append(pd.DataFrame(data[i], columns=list(['episode', 're1'])).melt(id_vars='episode',
                                                                        value_name='mean reward'))
    #print(label[i])
    df[i]['method'] = label[i]

fig, ax = plt.subplots(figsize=(25, 5))
df = pd.concat(df,ignore_index=True)  # 合并
#df = df[~df.index.duplicated()]
#df.to_csv('./df.csv')
sns.lineplot(x="episode", y="mean reward", hue="method", data=df, palette='bright')
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles[0:], labels=labels[0:])
plt.legend(loc=1)
font_set = FontProperties(fname=r"c:/Windows/fonts/simsun.ttc", size=12)
ax.set_xlabel(u'训练周期', fontproperties=font_set)
# ax.set_ylabel(u'累计奖励', fontproperties=font_set)
# ax.set_ylabel(u'决策步数', fontproperties=font_set)
ax.set_ylabel(u'损失', fontproperties=font_set)
plt.title('learning_rate = 1e-3') 
plt.savefig('gamma_loss1.svg', dpi=600, format='svg')
plt.show()
