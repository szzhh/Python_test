#2019 年上半年「万集科技」和「茅台」的收益率比较，比较指标包括
#日平均收益率
#收益率标准差
#收益率偏度
#收益率分布直方图

import tushare as ts
import matplotlib.pyplot as plt
from scipy.stats import skew

# 解决图表中文乱码
plt.rcParams['font.family'] = ['Noto Sans CJK JP']

# 按天获取 2019 年上半年万集股票的数据
wanji_data = ts.get_hist_data('300552', start='2019-01-02', end='2019-6-31', ktype='D')
# 将时间从小到大排序
wanji_data = wanji_data[::-1]
# 计算每一天的收益率
wanji_returns = wanji_data['close'].pct_change()
wanji_returns = wanji_returns.dropna()
# 计算平均收益率
wanji_returns_mean = wanji_returns.mean()
print('2019年上半年万集科技的日平均收益率是%f' % wanji_returns_mean)
# 计算标准差
wanji_returns_std = wanji_returns.std()
print('2019年上半年万集科技的收益率标准差是%f' % wanji_returns_std)
# 计算收益分布的偏度
wanji_returns_skewness = skew(wanji_returns)
print('2019年上半年万集科技收益率的偏度是%f' % wanji_returns_skewness)

# 按天获取 2019 年上半年茅台股票的数据
maotai_data = ts.get_hist_data('600519', start='2019-01-02', end='2019-6-31', ktype='D')
# 将时间从小到大排序
maotai_data = maotai_data[::-1]
# 计算每一天的收益率
maotai_returns = maotai_data['close'].pct_change()
maotai_returns = maotai_returns.dropna()
# 计算平均收益率
maotai_returns_mean = maotai_returns.mean()
print('2019年上半年茅台的日平均收益率是%f' % maotai_returns_mean)
# 计算标准差
maotai_returns_std = maotai_returns.std()
print('2019年上半年茅台的收益率标准差是%f' % maotai_returns_std)
# 计算收益分布的偏度
maotai_returns_skewness = skew(maotai_returns)
print('2019年上半年茅台收益率的偏度是%f：' % maotai_returns_skewness)

# 绘制万集科技收益率的分布直方图
plt.hist(wanji_returns, bins=75, label='万集科技')
# 绘制茅台收益率的分布直方图
plt.hist(maotai_returns, bins=75, label='茅台')

plt.legend(loc='best')
plt.show()
