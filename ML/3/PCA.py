# -*- coding:utf-8 -*-

import cv2
import numpy as np
import operator
import os
import scipy.io as sio
from PIL import Image, ImageDraw
import sklearn.decomposition

class PCA():
    def __init__(self, d):
        self.d = d

    def train(self, X):
        """
        Params: 
            X: np.array with shape (n, N).
        """
        X = np.array(X, dtype="float64")
        X = self.normalize(X)

        cov_matrix_t = X.T.dot(X)
        eigen_values, eigen_vectors = np.linalg.eig(cov_matrix_t) # the column v[:,i] is the eigenvector 
        eigen_values = eigen_values.tolist()
        eigen_vectors = X.dot(eigen_vectors)
        eigen_vectors = eigen_vectors.T.tolist()

        eigen_zip = [(value.real, vector) for value, vector in zip(eigen_values, eigen_vectors)]
        print ("len of real eigen values", len(eigen_zip))
        orderd_eigens = sorted(eigen_zip, key=operator.itemgetter(0), reverse=True)
        self.max_eigen_vectors = [orderd_eigens[i][1] for i in range(self.d)]
        self.W = np.real(np.array(self.max_eigen_vectors).T)        
        self.W /= np.sqrt(np.sum(self.W**2, axis=0, keepdims=True))

    def normalize(self, X):
        self.mean_vector = 1.0 / X.shape[1] * np.sum(X, axis=1, keepdims=True)     
        self.std = np.std(X, axis=1, keepdims=True) + 10e-8
        X = (X-self.mean_vector) # /(self.std)
        return X

    def dim_reduction(self, x):
        """
        Params:
            x: array with shape (n,1)
        """
        return self.W.T.dot(x)

    def construct(self, c):
        """
        Construct original image from encoder.
        """
        new =  self.W.dot(c)
        return (new)

def main():
    d = 20
    #path = "C:/Users/szh/Desktop/szh/Python_test/ML/3/yaleface"
    path='./yaleface'
    X = []
    n = 1
    for file in os.listdir(path):
        if not file.endswith(".txt") :
            img = Image.open(os.path.join(path, file))
            img = np.array(img).reshape(img.width*img.height)
            if n==1:
                first_img = img
            X.append(img)
            n+=1
    X = np.array(X)

    """ 调用sklearn中的PCA
    mu=np.mean(X, axis=0)
    pca1 = sklearn.decomposition.PCA()
    pca1.fit(X)
    xhat = np.dot(pca1.transform(first_img.reshape(1, -1))[:, :d], pca1.components_[:d, :])
    print "std pca W: ", pca1.components_
    xhat += mu
    img_array = np.array(xhat, dtype="int32").reshape(243, 320)
    img = Image.fromarray(img_array).convert("L")
    img.save("hh.png")
    print "std pca construct: ", img_array 
    """

    X = X.T
    pca = PCA(d)
    pca.train(X)
    print ("my pca W: ", pca.W )      
    for file in os.listdir(path):
        if not file.endswith(".txt") :
            img = Image.open(os.path.join(path, file))
            w, h = img.width, img.height
            img = np.array(img).reshape(w*h, 1)
            img = img - pca.mean_vector # 很重要
            features = pca.dim_reduction(img)
            x_hat = pca.construct(features)
            x_hat += pca.mean_vector # 很重要
            x_hat = x_hat.reshape(h, w)
            x_hat = np.array(x_hat, dtype="int32")
            new_img = Image.fromarray(x_hat).convert('L')
            new_file = file.split('.')[0]  + '.png'
            new_img.save(os.path.join('./output', new_file))
    cv2.imshow('降维前',cv2.imread('./yaleface/s1.bmp'))
    cv2.imshow('降维后',cv2.imread('./output/s1.png'))
    cv2.waitKey(0)



if __name__=="__main__":
    main()