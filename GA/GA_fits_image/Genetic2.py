# -*- coding: utf-8 -*-

from PIL import Image
import os
import math
import random
import pickle
from copy import deepcopy
from matplotlib import pyplot as plt
import cv2


# 读取图像
def GetImage(ori_img):
    img = Image.open(ori_img)
    #img = cv2.imread(ori_img)
    #img = Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    img = img.convert('RGB')
    color = []
    width, height = img.size
    for j in range(height):
        temp = []
        for i in range(width):
            r, g, b= img.getpixel((i, j))[:3]
            temp.append([r, g, b])    
        color.append(temp)
    return color, img.size


# 初始化
def RandGenes(size):
	width, height = size
	genes = []
	for i in range(100):
		gene = []
		for j in range(height):
			temp = []
			for i in range(width):
				r = random.randint(0, 255)
				g = random.randint(0, 255)
				b = random.randint(0, 255)
				temp.append([r, g, b])
			gene.append(temp)
		genes.append([gene, 0])
	return genes


# 计算适应度
def CalcFitness(genes, target):
	for k, gene in enumerate(genes):
		count = 0
		for i, row in enumerate(gene[0]):
			for j, col in enumerate(row):
				t_r, t_g, t_b= target[i][j]
				r, g, b= col
				count += (abs(t_r-r) + abs(t_g-g) + abs(t_b-b))
		genes[k][1] = round(float(count)/2700,4)
	genes.sort(key = lambda x: x[1])
	return genes


# 变异
def Variation(genes):
	rate = 0.5
	for k, gene in enumerate(genes):
		for i, row in enumerate(gene[0]):
			for j, col in enumerate(row):
				if random.random() < rate:
					liubo=gene[1]//10
					a = [-1, 1][random.randint(0, 1)] * random.randint(0,liubo)
					b = [-1, 1][random.randint(0, 1)] * random.randint(0,liubo)
					c = [-1, 1][random.randint(0, 1)] * random.randint(0,liubo)
					genes[k][0][i][j][0] += a
					genes[k][0][i][j][1] += b
					genes[k][0][i][j][2] += c
	return genes



# 交叉
def Merge(gene1, gene2, size):
	width, height = size
	y = random.randint(0, width-1)
	x = random.randint(0, height-1)
	new_gene = deepcopy(gene1[0][:x])
	new_gene = [new_gene, 0]
	new_gene[0][x:] = deepcopy(gene2[0][x:])
	new_gene[0][x][:y] = deepcopy(gene1[0][x][:y])
	return new_gene



# 自然选择
def Select(genes, size):
	seek = len(genes) * 2// 3
	i = 0
	j = seek + 1
	while i < seek:
		genes[j] = Merge(genes[i], genes[i+1], size)
		j += 1
		i += 2
	return genes



# 保存生成的图片
def SavePic(gene, generation, ori_img):
    gene = gene[0]
    img = Image.open(ori_img)
    img = img.convert('RGB')
    for j, row in enumerate(gene):
        for i, col in enumerate(row):
            r, g, b = col
            img.putpixel((i, j), (r, g, b))
    img.save("C:/Users/szh/Desktop/szh/Python_test/GA/GA_fits_image/test8/{}.png".format(generation))



# 备份
def SaveData(data, backup):
	print('[INFO]: Save data to {}...'.format(backup))
	with open(backup, 'wb') as f:
		pickle.dump(data, f)
	f.close()


# 读取备份
def ReadData(backup):
	print('[INFO]: Read data from {}...'.format(backup))
	with open(backup, 'rb') as f:
		data = pickle.load(f)
		genes = data['gene']
		generation = data['generation']
		best=data['best']
		worst=data['worst']
		avg=data['avg']
	f.close()
	return genes, generation,best,worst,avg

#绘图
def draw(generation,best,worst,avg):
	plt.rcParams['font.sans-serif']=['SimHei']
	plt.rcParams['axes.unicode_minus'] = False
	plt.plot(range(generation),best,color='red')
	plt.plot(range(generation),worst,color='blue')
	plt.plot(range(generation),avg,color='green')
	plt.xlabel('进化代数')
	plt.ylabel('适应度值')
	plt.title('适应度值变化图')
	plt.legend(['Best','Worst','Average'])
	#plt.show()
	plt.ion()
	plt.pause(0.01)

# 运行
def run(ori_img, backup, resume):
	data, size = GetImage(ori_img)
	if resume:
		genes, generation, best, worst, avg= ReadData(backup)
	else:
		genes = RandGenes(size)
		generation = 0
		best=[]
		worst=[]
		avg=[]
	while True:
		generation += 1
		genes = CalcFitness(genes, data)
		fitsum=0
		for i in range (100):
			fitsum+=genes[i][1]
		Averagefit=round(float(fitsum)/100,4)
		print('Generation: {}, Best: {:.4f}, Worst: {:.4f}, Average: {:.4f}'.format(generation, genes[0][1], genes[99][1],Averagefit))
		best.append(genes[0][1])
		worst.append(genes[99][1])
		avg.append(Averagefit)
		#draw(generation,best,worst,avg)
		genes = Select(genes, size)
		genes = Variation(genes)
		if generation % 50 == 0:
			SaveData({'gene': genes, 'generation': generation, 'best':best, 'worst':worst, 'avg':avg}, backup)
			SavePic(genes[0], generation, ori_img)



if __name__ == '__main__':
	# 备份
	backup = 'C:/Users/szh/Desktop/szh/Python_test/GA/GA_fits_image/test8/backup.tmp'
	# 原始图像
	ori_img ='C:/Users/szh/Desktop/szh/Python_test/GA/GA_fits_image/test.png'
	# resume为True则读取备份文件，在其基础上进行自然选择，交叉变异
	run(ori_img, backup, resume=False)
