# coding: utf-8
import csv
import re

class CutWords:

    def __init__(self):
        dict_path = './dict.txt'
        self.word_dict = self.load_words(dict_path)

    #加载词典
    def load_words(self, dict_path):
        words = list()
        words_dic = {} #字典速度较快
        for line in open('./train.csv',encoding="utf-8"):
            words += line.strip().split(' ')
        for line in open('./OOV_dict.csv',encoding="utf-8"):
            words += line.strip().split(' ')
        for line in open('./train.txt',encoding="utf-8"):
            words += line.strip().split(' ')
        for line in open(dict_path,encoding="utf-8"):
            words += line.strip().split(' ')
        for i in range(len(words)):
            words_dic[words[i]]=i
        print(len(words))
        print(len(words_dic))
        return words_dic

    #最大向前匹配
    def max_forward_cut(self, sent):
        #1.从左向右取待切分汉语句的m个字符作为匹配字段，m为大机器词典中最长词条个数。
        #2.查找大机器词典并进行匹配。若匹配成功，则将这个匹配字段作为一个词切分出来。
        cutlist = []
        index = 0
        max_wordlen = 8
        while index < len(sent):
            matched = False
            for i in range(max_wordlen, 0, -1):
                cand_word = sent[index : index + i]
                if cand_word in self.word_dict:
                    cutlist.append(cand_word)
                    matched = True
                    break
    
            #如果没有匹配上，则按字符切分
            if not matched:
                i = 1
                cutlist.append(sent[index])
            index += i
        return cutlist
    
    #最大向后匹配
    def max_backward_cut(self, sent):
        #1.从右向左取待切分汉语句的m个字符作为匹配字段，m为大机器词典中最长词条个数。
        #2.查找大机器词典并进行匹配。若匹配成功，则将这个匹配字段作为一个词切分出来。
        cutlist = []
        index = len(sent)
        max_wordlen = 10
        while index > 0 :
            matched = False
            for i in range(max_wordlen, 0, -1):
                tmp = (i + 1)
                cand_word = sent[index - tmp : index]
                #如果匹配上，则将字典中的字符加入到切分字符中
                if cand_word in self.word_dict:
                    cutlist.append(cand_word)
                    matched = True
                    break
            #如果没有匹配上，则按字符切分
            if not matched:
                tmp = 1
                cutlist.append(sent[index-1])
    
            index -= tmp
    
        return cutlist[::-1]

    # 双向最大向前匹配
    def max_biward_cut(self, sent):
        # 双向最大匹配法是将正向最大匹配法得到的分词结果和逆向最大匹配法的到的结果进行比较，从而决定正确的分词方法。
        # 启发式规则：
        # 1.如果正反向分词结果词数不同，则取分词数量较少的那个。
        # 2.如果分词结果词数相同 a.分词结果相同，就说明没有歧义，可返回任意一个。 b.分词结果不同，返回其中单字较少的那个。
        forward_cutlist = self.max_forward_cut(sent)
        backward_cutlist = self.max_backward_cut(sent)
        count_forward = len(forward_cutlist)
        count_backward = len(backward_cutlist)
    
        def compute_single(word_list):
            num = 0
            for word in word_list:
                if len(word) == 1:
                    num += 1
            return num
    
        if count_forward == count_backward:
            if compute_single(forward_cutlist) < compute_single(backward_cutlist):
                return backward_cutlist
            else:
                return forward_cutlist
    
        elif count_backward < count_forward:
            return forward_cutlist
    
        else:
            return backward_cutlist

def transfer(raw_sen):
    count = 0
    tmp_list = []
    for ele in raw_sen.strip().split(' '):
        _tmp_list = []
        for _ in range(len(ele)):
            _tmp_list.append(count)
            count += 1
        tmp_list.append(str(_tmp_list).replace(' ', ''))
    return ' '.join(tmp_list)



# 读取csv至字典
csvFile = open("test.csv", encoding='utf-8',)
reader = csv.reader(csvFile)

# 建立空字典
senlst = []
for item in reader:
    # 忽略第一行
    if reader.line_num == 1:
        continue
    senlst.append(item[1])
    
csvFile.close()

cuter = CutWords()
result=[]
n=1
for item in senlst:
    result.append([str(n),transfer(' '.join(cuter.max_forward_cut(item)))])
    # result.append([str(n),transfer(' '.join(cuter.max_backward_cut(item)))])
    # result.append([str(n),transfer(' '.join(cuter.max_biward_cut(item)))])
    n+=1

print(senlst[370])
print(result[370])

fileHeader = ["id", "expected"]
csvFile = open("./result.csv", "w",newline='')
writer = csv.writer(csvFile)
writer.writerow(fileHeader)
for item in result:
    writer.writerow(item)

csvFile.close()

#计算f1
csvFile = open("result.csv", encoding='utf-8',)
reader = csv.reader(csvFile)
lst = []
for item in reader:
    # 忽略第一行
    if reader.line_num == 1:
        continue
    lst.append(item[1])
csvFile.close()
n=0
f1=[]
for line in open('./sample.csv',encoding="utf-8"):
    A=lst[n].split(' ')
    B=[]
    B+=line.strip('"\n').split(' ')
    A=set(A)
    B=set(B)     
    A_size = len(A)
    B_size = len(B)
    A_cap_B_size = len(A & B)
    p, r = A_cap_B_size / B_size * 100, A_cap_B_size / A_size * 100
    if p+r==0:
        f1.append(0)
    else:        
        f1.append(2 * p * r / (p + r))
    n+=1
print(sum(f1)/n)
csvFile = open("./f1.csv", "w",newline='')
writer = csv.writer(csvFile)
for item in f1:
    writer.writerow([str(item)])
csvFile.close()

