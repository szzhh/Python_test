import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import *

#下采样
def dataProcess(data):
    # Shuffle the Dataset.
    shuffled_df = data.sample(frac=1,random_state=4)
    # Put all the fraud class in a separate dataset.
    fraud_df = shuffled_df.loc[shuffled_df['Churn?'] == 'True.']
    #Randomly select 483 observations from the non-fraud (majority class)
    non_fraud_df=shuffled_df.loc[shuffled_df['Churn?']== 'False.'].sample(n=483,random_state=42)
    # Concatenate both dataframes again
    normalized_df = pd.concat([fraud_df, non_fraud_df])
    return normalized_df
#准确率
def accuracy(y_true,y_pred):
    return np.mean(y_true == y_pred) 

#绘制ROC曲线
def draw_roc(y1,y2,acc1,y3,y4,acc2,str,n):
    plt.figure(n)
    fpr, tpr, thresholds=roc_curve(y1,y2,pos_label=1)
    aucs=auc(fpr,tpr)
    plt.plot(fpr,tpr, lw=1.5, c='r', label="无特征提取 ACC={:.5f} AUC={:.3f}".format(acc1,aucs))
    fpr, tpr, thresholds=roc_curve(y3,y4,pos_label=1)
    aucs=auc(fpr,tpr)
    plt.plot(fpr,tpr, lw=1.5, c='b', label="有特征提取 ACC={:.5f} AUC={:.3f}".format(acc2,aucs))
    plt.plot([0, 1], [0, 1], c='k', linestyle='--')
    plt.xlabel("FPR",fontsize=15)
    plt.ylabel("TPR",fontsize=15)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.xlim(-0.1,1)
    plt.ylim(0,1.1)
    plt.title(str+"ROC曲线")
    plt.legend(loc="lower right")
    # plt.show()
    
#绘制ROC曲线
def draw_roc1(y1,y2,acc1,y3,y4,acc2,str,n):
    plt.figure(n)
    fpr, tpr, thresholds=roc_curve(y1,y2,pos_label=1)
    aucs=auc(fpr,tpr)
    plt.plot(fpr,tpr, lw=1.5, c='r', label="改进前 ACC={:.5f} AUC={:.3f}".format(acc1,aucs))
    fpr, tpr, thresholds=roc_curve(y3,y4,pos_label=1)
    aucs=auc(fpr,tpr)
    plt.plot(fpr,tpr, lw=1.5, c='b', label="改进后 ACC={:.5f} AUC={:.3f}".format(acc2,aucs))
    plt.plot([0, 1], [0, 1], c='k', linestyle='--')
    plt.xlabel("FPR",fontsize=15)
    plt.ylabel("TPR",fontsize=15)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.xlim(-0.1,1)
    plt.ylim(0,1.1)
    plt.title(str+"ROC曲线")
    plt.legend(loc="lower right")
    # plt.show()