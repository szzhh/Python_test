from PIL import Image
import os
import math
import random
import pickle
from copy import deepcopy
from matplotlib import pyplot as plt
import time

# 读取图像
def GetImage(ori_img):
    img = Image.open(ori_img)
    color = []
    width, height = img.size
    for j in range(height):
        temp = []
        for i in range(width):
            r= img.getpixel((i, j))[:1]
            temp.append([r[0],r[0]])
        color.append(temp)
    # for j in range(height):
    #     for i in range(width):
    #         print(" ", end="")
    #         print(color[i][j][0],end="")
    #         print(" ", end="")
    #     print("",end="\n")
    # color：三维数组，第一维列表包含r,g,b,r+g+b四个值，第二维表示行，第三维表示列
    return color, img.size


# 初始化
def RandGenes(size, target):
    width, height = size
    genes = []
    for i in range(100):
        gene = []
        for j in range(height):
            temp = []
            for k in range(width):
                t_r, t_a = target[j][k]
                r = random.randint(0, 255)
                a = abs(t_r - r)
                temp.append([r,a])
            gene.append(temp)
        genes.append([gene, 0])
    # genes：三维数组，[[基因],适应度]，基因：[[每行]]，每行：[[每列]]，每列：[r,g,b,rgb总差值]
    return genes


# 计算适应度
def CalcFitness(genes, target):
    # total = 0
    for k, gene in enumerate(genes):
        count = 0
        for i, row in enumerate(gene[0]):
            for j, col in enumerate(row):
                t_r,  t_a = target[i][j]
                r, a = col
                a = abs(t_r - r)
                count += a
        genes[k][1] = count
        # total += count
    genes.sort(key=lambda x: x[1])
    return genes


# 总体变异
def Variation(genes, target,generation):
    for k, gene in enumerate(genes):
        genes[k] = AltOffspring(genes[k], target,generation)
    return genes


# 个体变异
def SelfVariation(parent,  t_b,generation):
    if generation<10:
        # 较大变异，概率较小
        max_mutate_rate = 0.2
        mid_mutate_rate = 0.4
        # 较小变异，概率较大
        min_mutate_rate = 1
    else:
        # 较大变异，概率较小
        max_mutate_rate = 0.05
        mid_mutate_rate = 0.2
        # 较小变异，概率较大
        min_mutate_rate = 0.8
    offspring = deepcopy(parent)
    if random.random() < max_mutate_rate and generation<10:
        offspring[0] = random.randint(0, 255)

    if random.random() < mid_mutate_rate and generation<10:
        offspring[0] = min(max(0, offspring[0] + random.randint(-30, 30)), 255)

    if random.random() < min_mutate_rate and generation<10:
        offspring[0] = min(max(0, offspring[0] + random.randint(-10, 10)), 255)

    if random.random() < max_mutate_rate and generation>10:
        offspring[0] = random.randint(0, 255)

    if random.random() < mid_mutate_rate and generation>10:
        offspring[0] = min(max(0, offspring[0] + random.randint(-15, 15)), 255)

    if random.random() < min_mutate_rate and generation>10:
        offspring[0] = min(max(0, offspring[0] + random.randint(-5, 5)), 255)

    offspring[1] = abs(offspring[0] - t_b)
    return offspring


# 子代父代最优取代
def AltOffspring(gene, target,generation):
    for i, row in enumerate(gene[0]):
        for j, parent in enumerate(row):
            p_r,p_a = parent
            t_r, t_a = target[i][j]
            offsprings = []
            for k in range(5):
                offsprings.append(SelfVariation(parent, t_r,generation))
            # 按照第四维排序
            offsprings.sort(key=lambda x: x[1])
            gene[0][i][j] = offsprings[0] if offsprings[0][1] < p_a else parent
    return gene

#  交叉
def Merge(gene1, gene2, size):
    width, height = size
    y = random.randint(0, width - 1)
    x = random.randint(0, height - 1)
    new_gene = deepcopy(gene1[0][:x])
    new_gene = [new_gene, 0]
    new_gene[0][x:] = deepcopy(gene2[0][x:])
    new_gene[0][x][:y] = deepcopy(gene1[0][x][:y])
    return new_gene


#  自然选择
def Select(genes, size):
    # print(genes.shape)
    seek = len(genes) * 2 // 3
    i = 0
    j = seek + 1
    # 将后1/3的基因替换为前2/3基因的两两交叉
    while i < seek:
        # 锦标赛法
        parent1=findGreatParent(genes)
        parent2=findGreatParent(genes)
        genes[j] = Merge(parent1, parent2, size)
        j += 1
        i += 2
    return genes

def findGreatParent(genes):
    list=[]
    for _ in range(10):
        list.append(random.randint(0, 67))
    # print(list)
    genesList=[]
    for i in range(10):
        genesList.append(genes[list[i]])
    genesList.sort(key=lambda x: x[1])
    # print(genesList)
    return genesList[0]


def SavePlotData(genes, generation, plotdata):
    fitnessSum = 0
    for i in range(100):
        fitnessSum += genes[i][1]
    plotdata[0].append(genes[0][1])
    plotdata[1].append(genes[99][1])
    plotdata[2].append(fitnessSum / 100)
    plotdata[3].append(generation)
    plt.plot(plotdata[3], plotdata[0], color='red', label='best')
    plt.plot(plotdata[3], plotdata[1], color='green', label='worst')
    plt.plot(plotdata[3], plotdata[2], color='blue', linestyle='--', label='average')
    plt.xlabel('generation')
    plt.ylabel('fitness')
    plt.savefig('{}.png'.format('fitness' + str(generation)))
    plt.show()


# 保存生成的图片
def SavePic(gene, generation, ori_img):
    gene = gene[0]
    img = Image.open(ori_img)
    #img = img.convert('RGB')
    for j, row in enumerate(gene):
            for i, col in enumerate(row):
                r,  _ = col
                img.putpixel((i, j), (r, r, r))
    img.save(os.path.splitext(ori_img)[0]+'/{}.png'.format(generation))
    print('Save {}.png to '.format(generation)+os.path.splitext(ori_img)[0])



# 备份
def SaveData(data, backup):
    if  not os.path.exists(os.path.dirname(backup)):
        os.mkdir(os.path.dirname(backup))
    print('Save data to {}...'.format(backup))
    with open(backup, 'wb') as f:
        pickle.dump(data, f)
    f.close()


# 读取备份
def ReadData(backup):
	print('Read data from {}...'.format(backup))
	with open(backup, 'rb') as f:
		data = pickle.load(f)
		genes = data['gene']
		generation = data['generation']
		best=data['best']
		worst=data['worst']
		avg=data['avg']
	f.close()
	return genes, generation,best,worst,avg


# 运行
def run(ori_img, backup, plotdata, resume=False):
    data, size = GetImage(ori_img)
    if resume:
        genes, generation = ReadData(backup)
    else:
        genes = RandGenes(size, data)
        generation = 0
    genes = CalcFitness(genes, data)
    # t0 = time.time()
    while True:
        genes = Variation(genes, data)
        genes = Select(genes, size)
        genes = CalcFitness(genes, data)
        generation += 1
        # if generation % 10 == 0:
        # print(time.time() - t0, "seconds wall time")
        SaveData({'genes': genes, 'generation': generation}, backup)
        # SavePic([genes[0]], generation, ori_img)
        SavePic([genes[0], genes[50], genes[99]], generation, ori_img)
        #SavePlotData(genes, generation, plotdata)
        print('<Generation>: {}, <Select3>: {:.4f} {:.4f} {:.4f}'.format(generation, genes[0][1], genes[50][1],
                                                                        genes[99][1]))
        if(genes[0][1]==0 and genes[50][1]==0 and genes[99][1]==0):
            break

