# 对曲线进行平滑处理，weight参数与tensorboard的Smoothing相同

import pandas as pd
import numpy as np
import os


def smooth(csv_path, weight=0.9):
    data = pd.read_csv(filepath_or_buffer=csv_path, header=0, names=['Step', 'Value'],dtype={'Step': int, 'Value': float})
    scalar = data['Value'].values
    last = scalar[0]
    smoothed = []
    for point in scalar:
        smoothed_val = last * weight + (1 - weight) * point
        smoothed.append(smoothed_val)
        last = smoothed_val

    save = pd.DataFrame({'Step':data['Step'].values,'Value':smoothed})
    return save


if __name__ == '__main__':
    save = smooth('./result1/1_94_loss.csv')
    save.to_csv('./smooth1/1_94_loss.csv')


