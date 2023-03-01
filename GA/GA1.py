#代码参考：https://blog.csdn.net/ha_ha_ha233/article/details/91364937
import numpy as np #用于数据操作：【X = np.linspace(*X_BOUND, 100)  #将列表传入收集参数，完成解包】【 Y = np.linspace(*Y_BOUND, 100)】【X, Y = np.meshgrid(X, Y)  #生成网格点坐标矩阵，每个二维矩阵表示一个维度】
import matplotlib.pyplot as plt #用于画图，可画二维【fig = plt.figure()】、三维【ax = fig.add_subplot(111, projection='3d')】；亦可上色【ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap = plt.get_cmap('rainbow'))】
from matplotlib import cm   #绘制3d曲面时用于给图上色：【ax.plot_surface(X, Y, Z, rstride = 1, cstride = 1, cmap = cm.coolwarm)】
from mpl_toolkits.mplot3d import Axes3D #用于画三维图，将二维图变换为三维图： 【fig = plt.figure()】  【ax = Axes3D(fig)】


DNA_SIZE = 24
POP_SIZE = 200
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.005
N_GENERATIONS = 50
X_BOUND = [-3, 3]
Y_BOUND = [-3, 3]


def F(x, y):
    return 3 * (1 - x) ** 2 * np.exp(-(x ** 2) - (y + 1) ** 2) - 10 * (x / 5 - x ** 3 - y ** 5) * np.exp(
        -x ** 2 - y ** 2) - 1 / 3 ** np.exp(-(x + 1) ** 2 - y ** 2)


def translateDNA(pop):  # pop表示种群矩阵，一行表示一个二进制编码表示的DNA，矩阵的行数为种群数目
    x_pop = pop[:, 1::2]  # 奇数列表示X
    y_pop = pop[:, ::2]  # 偶数列表示y
    '''
    dot()表示矩阵相乘；*表示点积与MATLAB.*相似
    '''
    # pop:(POP_SIZE,DNA_SIZE)*(DNA_SIZE,1) --> (POP_SIZE,1)
    x = x_pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) / float(2 ** DNA_SIZE - 1) * (X_BOUND[1] - X_BOUND[0]) + X_BOUND[0]   #dot()表示矩阵相乘；*表示点积与MATLAB.*相似
    y = y_pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) / float(2 ** DNA_SIZE - 1) * (Y_BOUND[1] - Y_BOUND[0]) + Y_BOUND[0]
    return x, y



    '''
    #最小值适应度函数
    def get_fitness(pop): 
	x,y = translateDNA(pop)
	pred = F(x, y)
	return -(pred - np.max(pred)) + 1e-3
    '''
#最大值适应度函数
def get_fitness(pop):
    x, y = translateDNA(pop)
    pred = F(x, y)
    '''
    #np.min用法
    import numpy as np  
    a = np.array([[1,5,3],[4,2,6]])  
    print(a.min()) #无参，所有中的最小值   print(min(a))
    print(a.min(0)) # axis=0; 每列的最小值  print(min(a, axis = 0))
    print(a.min(1)) # axis=1；每行的最小值  print(min(a, axis = 1))
    '''
    return (pred - np.min(pred)) + 1e-3  # 减去最小的适应度是为了防止适应度出现负数，通过这一步fitness的范围为[0, np.max(pred)-np.min(pred)]

def select(pop, fitness):  # nature selection wrt pop's fitness
    idx = np.random.choice(np.arange(POP_SIZE), size=POP_SIZE, replace=True,p=(fitness) / (fitness.sum()))
    '''
    #np.random.choice()用法
    1、参数意思分别 是从a 中以概率P，随机选择3个, p没有指定的时候相当于是一致的分布，a为一维数组或int，如果是int，则生成随机样本，就好像a是np.arange(N)一样。
        a1 = np.random.choice(a=5, size=3, replace=False, p=None)
    2、非一致的分布，会以多少的概率提出来
        a2 = np.random.choice(a=5, size=3, replace=False, p=[0.2, 0.1, 0.3, 0.4, 0.0])
    replacement 代表的意思是抽样之后还放不放回去，如果是False的话，那么出来的三个数都不一样，如果是True的话， 有可能会出现重复的，因为前面的抽的放回去了。
    '''
    return pop[idx]


def crossover_and_mutation(pop, CROSSOVER_RATE=0.8):
    new_pop = []
    for father in pop:  # 遍历种群中的每一个个体，将该个体作为父亲
        child = father  # 孩子先得到父亲的全部基因（这里我把一串二进制串的那些0，1称为基因）
        '''
        【1】 np.random.rand()
            注：使用方法与np.random.randn()函数相同 
            作用： 通过本函数可以返回一个或一组服从“0~1”均匀分布的随机样本值。随机样本取值范围是[0,1)，不包括1。
        【2】np.random.randn(d0,d1,d2……dn) 
            1)当函数括号内没有参数时，则返回一个浮点数； 
            2）当函数括号内有一个参数时，则返回秩为1的数组，不能表示向量和矩阵； 
            3）当函数括号内有两个及以上参数时，则返回对应维度的数组，能表示向量或矩阵； 
            4）np.random.standard_normal（）函数与np.random.randn()类似，但是np.random.standard_normal（）
            的输入参数为元组（tuple）. 
            5)np.random.randn()的输入通常为整数，但是如果为浮点数，则会自动直接截断转换为整数。
            作用：通过本函数可以返回一个或一组服从标准正态分布的随机样本值。
        【3】np.random.randint()
            numpy.random.randint(low, high=None, size=None, dtype=’l’) 
            输入： 
            low—–为最小值 
            high—-为最大值 
            size—–为数组维度大小 
            dtype—为数据类型，默认的数据类型是np.int。 
            返回值： 
            返回随机整数或整型数组，范围区间为[low,high），包含low，不包含high； 
            high没有填写时，默认生成随机数的范围是[0，low）
        更多详情：https://www.cnblogs.com/fpzs/p/10288239.html
        '''
        if np.random.rand() < CROSSOVER_RATE:  # 产生子代时不是必然发生交叉，而是以一定的概率发生交叉
            mother = pop[np.random.randint(POP_SIZE)]  # 再种群中选择另一个个体，并将该个体作为母亲
            cross_points = np.random.randint(low=0, high=DNA_SIZE * 2)  # 随机产生交叉的点
            child[cross_points:] = mother[cross_points:]  # 孩子得到位于交叉点后的母亲的基因
        mutation(child)  # 每个后代有一定的机率发生变异
        new_pop.append(child)
    return new_pop


def mutation(child, MUTATION_RATE=0.003):
    if np.random.rand() < MUTATION_RATE:  # 以MUTATION_RATE的概率进行变异
        mutate_point = np.random.randint(0, DNA_SIZE*2)  # 随机产生一个实数，代表要变异基因的位置
        '''
        ^1表示异或（不同为1），实现反转
        '''
        child[mutate_point] = child[mutate_point] ^ 1  # 将变异点的二进制为反转


def plot_3d(ax):
    X = np.linspace(*X_BOUND, 100)  #将列表传入收集参数，完成解包
    Y = np.linspace(*Y_BOUND, 100)
    X, Y = np.meshgrid(X, Y)  #生成网格点坐标矩阵，每个二维矩阵表示一个维度
    Z = F(X, Y)
    '''
    绘制3D曲面
    
    rstride:行之间的跨度  cstride:列之间的跨度
    rcount:设置间隔个数，默认50个，ccount:列的间隔个数  不能与上面两个参数同时出现
    
    cmap是颜色映射表
    # from matplotlib import cm
    # ax.plot_surface(X, Y, Z, rstride = 1, cstride = 1, cmap = cm.coolwarm)
    # cmap = "rainbow" 亦可
    我的理解的 改变cmap参数可以控制三维曲面的颜色组合, 一般我们见到的三维曲面就是 rainbow 的
    你也可以修改 rainbow 为 coolwarm, 验证我的结论
    '''
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap = plt.get_cmap('rainbow'))
    '''
    # 绘制从3D曲面到底部的投影,zdir 可选 'z'|'x'|'y'| 分别表示投影到z,x,y平面
    # zdir = 'z', offset = -2 表示投影到z = -2上
    ax.contour(X, Y, Z, zdir = 'z', offset = -2, cmap = plt.get_cmap('rainbow'))
    '''
    ax.contour(X, Y, Z, zdir='z', offset=-10, cmap=plt.get_cmap('rainbow'))
    # 设置z轴的维度，x,y类似
    ax.set_zlim(-10, 10)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    '''
    plt.pause(time)函数也能实现窗口绘图（不需要plt.show）,但窗口只停留time时间便会自动关闭，然后再继续执行后面代码；
    plt.pause()会把它之前的所有绘图都绘制在对应坐标系中，而不仅仅是在当前坐标系中绘图；
    特别要注意的是，plt.pasue(0)将绘制之前的所有图像，且图像窗口不会自动关闭，但程序会停止在该语句所在位置，即使手动关闭窗口也不会继续执行后面的代码。
    '''
    #plt.pause(3) #显示图片，但最后会停顿一会儿后关闭
    '''
    这里的plt.show()主要与后面的plt.ioff()配合使用，否则最后的图会一闪而过不会停留
    '''
    plt.show()  #一直显示图片；最后不关闭图，代码不会结束运行


def print_info(pop):
    fitness = get_fitness(pop)
    max_fitness_index = np.argmax(fitness)
    print("max_fitness:", fitness[max_fitness_index])
    x, y = translateDNA(pop)
    print("最优的基因型：", pop[max_fitness_index])
    print("(x, y):", (x[max_fitness_index], y[max_fitness_index]))


if __name__ == "__main__":
    #定义figure
    fig = plt.figure()
    #创建3d图形的两种方式
    #将figure变为到3d
    #ax = Axes3D(fig)
    ax = fig.add_subplot(111, projection='3d')  #111表示1x1网格，第一子图
    plt.ion()  # 将画图模式改为交互模式，程序遇到plt.show不会暂停，而是继续执行
    plot_3d(ax)

    pop = np.random.randint(2, size=(POP_SIZE, DNA_SIZE * 2))  # matrix (POP_SIZE, DNA_SIZE)
    #numpy.random.randint(low, high=None, size=None, dtype='l')  函数的作用是，返回一个随机整型数，范围从低（包括）到高（不包括），即[low, high)。如果没有写参数high的值，则返回[0,low)的值。
    for _ in range(N_GENERATIONS):  # 迭代N代
        x, y = translateDNA(pop)
        if 'sca' in locals():  #当你定义了一堆变量，locals()就能看见里面有你定义的变量表
            sca.remove()
        sca = ax.scatter(x, y, F(x, y), c='black', marker='o');  #画散点图   https://blog.csdn.net/qiu931110/article/details/68130199/
        plt.show();
        plt.pause(0.1)
        pop = np.array(crossover_and_mutation(pop, CROSSOVER_RATE))
        # F_values = F(translateDNA(pop)[0], translateDNA(pop)[1])#x, y --> Z matrix
        fitness = get_fitness(pop)
        pop = select(pop, fitness)  # 选择生成新的种群

    print_info(pop)
    plt.ioff()  #如果在脚本中使用ion()命令开启了交互模式，没有使用ioff()关闭的话，则图像会一闪而过，并不会常留。要想防止这种情况，需要在plt.show()之前加上ioff()命令。
    plot_3d(ax)

