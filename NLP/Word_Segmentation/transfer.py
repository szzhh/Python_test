"""
    切分结果转换脚本。
    param:
        raw_sen: 切分结果，由空格隔开的字符串。“我 爱 自然 语言 处理”

    return：
        转换为序列的字符串。"[0] [1] [2,3] [4,5] [6,7]"
"""

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
    
if __name__=="__main__":
    print(transfer('我 爱 自然 语言 处理'))