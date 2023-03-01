# 遗传算法进化出Chrome浏览器图标
from PIL import Image
import os
import math
import random
import pickle
from copy import deepcopy


# 读取图像
def GetImage(ori_img):
	img = Image.open(ori_img)
	color = []
	width, height = img.size
	for j in range(height):
		temp = []
		for i in range(width):
			r, g, b = img.getpixel((i, j))[:3]
			temp.append([r, g, b, r+g+b])
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
				temp.append([r, g, b, r+g+b])
			gene.append(temp)
		genes.append([gene, 0])
	return genes


# 计算适应度
def CalcFitness(genes, target):
	total = 0
	for k, gene in enumerate(genes):
		count = 0
		for i, row in enumerate(gene[0]):
			for j, col in enumerate(row):
				t_r, t_g, t_b, t_a = target[i][j]
				r, g, b, a = col
				diff = abs(t_a - a)
				count += (abs(t_r-r) + abs(t_g-g) + abs(t_b-b)) * diff
		genes[k][1] = count
		total += count
	avg_total = total / (k+1)
	for k, gene in enumerate(genes):
		genes[k][1] = genes[k][1] / avg_total
	genes.sort(key = lambda x: x[1],reverse = False)
	return genes


# 变异
def Variation(genes):
	rate = 0.1
	for k, gene in enumerate(genes):
		for i, row in enumerate(gene[0]):
			for j, col in enumerate(row):
				if random.random() < rate:
					a = [-1, 1][random.randint(0, 1)] * random.randint(3, 10)
					b = [-1, 1][random.randint(0, 1)] * random.randint(3, 10)
					c = [-1, 1][random.randint(0, 1)] * random.randint(3, 10)
					genes[k][0][i][j][0] += a
					genes[k][0][i][j][1] += b
					genes[k][0][i][j][2] += c
					genes[k][0][i][j][3] += a + b + c
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
	seek = len(genes) * 2 // 3
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
	for j, row in enumerate(gene):
		for i, col in enumerate(row):
			r, g, b, _ = col
			img.putpixel((i, j), (r, g, b))
	img.save("C:/Users/szh/Desktop/szh/Python_test/GA/GA_fits_image/test1/{}.png".format(generation))


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
		genes = data['genes']
		generation = data['generation']
	f.close()
	return genes, generation


# 运行
def run(ori_img, backup, resume=False):
	data, size = GetImage(ori_img)
	if resume:
		genes, generation = ReadData(backup)
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
		plt.plot(range(generation),best,color='red')
		plt.plot(range(generation),worst,color='blue')
		plt.plot(range(generation),avg,color='green')
		plt.show()
		genes = Select(genes, size)
		genes = Variation(genes)
		if generation % 50 == 0:
			SaveData({'gene': genes, 'generation': generation}, backup)
			SavePic(genes[0], generation, ori_img)


if __name__ == '__main__':
	# 备份
	backup = 'C:/Users/szh/Desktop/szh/Python_test/GA/GA_fits_image/backup.tmp'
	# 原始图像
	ori_img ='C:/Users/szh/Desktop/szh/Python_test/GA/GA_fits_image/test.png'
	# resume为True则读取备份文件，在其基础上进行自然选择，交叉变异
	run(ori_img, backup, resume=False)