#使用专家系统来构建 动物识别系统

#使用：加入一条规则S，当规则库中已有的node中包含了S的前置条件，才加入到规则库中，否则先跳过
def TopulogyRules(rules):
    basicAttr = set()   #基础属性
    midAttr = set()     #这些中是被推倒出来的结论
    for rule in rules:
        for attr in rule:
            basicAttr.add(attr)
        midAttr.add(rule[-1])
    basicAttr = basicAttr - midAttr     #全部属性 - 中间属性 = 基础属性
    
    rs = rules.copy()
    visited = []
    for i in range(len(rules)):
        visited.append(0)
    newRules = []
    while(len(rs) != 0): 
        for rule in rules:
            if rule in rs:
                s = set(rule[:-1])
                if s <= basicAttr:
                    newRules.append(rule)
                    rs.remove(rule)
                    visited[i] = 1
                    basicAttr.add(rule[-1])
    #print(newRules)
    #不断新建base环境，不断向前搜索，不断添加
    return rules

###读入rules.txt，然后拓扑化 rules，返回一个拓扑化之后的 rules
def getRules():
    animalKinds = []
    rules = []
    f = open("./rules.txt", 'r', encoding='UTF-8')
    #f = open("./AnimalRecongnizeSystem/data.txt", 'r').read()
    for line in f:
        #print(line, end='')
        line = line.replace("\n","")
        ls = line.split(" ")
        rules.append(ls)
    animalKinds = rules[-1]
    rules.pop()
    rules = TopulogyRules(rules)
    f.close()
    return rules,animalKinds

def getAnimalInfo():
    info = input("请输入动物的特征(空格为分隔符): ")
    basicInfo = info.split(' ')
    return basicInfo

def Inference(rules, basicInfo, animalKinds):
    animal = "无法识别"
    for rule in rules:
        set1 = set(rule[:-1])
        set2 = set(basicInfo)
        if set1 <= set2:
            set2.add(rule[-1])
            basicInfo = list(set2)
            if rule[-1] in animalKinds:
                animal = rule[-1]
                break
    print(basicInfo)
    return animal

def showRules():
    pass

def main():
    rules, animalKinds = getRules()
    print('-----------------------------------------------------------------------------------------')
    print("知识库中的全部规则为:\n{}".format(rules))
    print('-----------------------------------------------------------------------------------------')
    print("知识库能推导出的动物种类为:{}".format(animalKinds))
    print('-----------------------------------------------------------------------------------------')
    basicInfo = getAnimalInfo()
    animal = Inference(rules, basicInfo, animalKinds)
    print("你描述的动物是:{}".format(animal))
    
if __name__ == '__main__':
    main()

# 测试用例:身上有暗斑点 黄褐色 长脖子 有长腿 有奶 有蹄