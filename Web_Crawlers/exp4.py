import time
import requests
import re
from openpyxl import workbook
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup as bs

class Top250:
    def __init__(self):
        #起始地址
        self.start_url = 'https://movie.douban.com/top250'
        #请求头，浏览器模拟
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        }
        #爬取页数
        self.page_num = 10

##    url拼接
        
    def get_page_url(self):
        n = 0 #第一页开始,下标0
        while n<self.page_num:
            yield self.start_url+'?start={}&filter='.format(n*25)
            n += 1

##    获取页面源码
            
    def getHtml(self):
        gu = self.get_page_url() #url生成器
        for url in gu:
            html = requests.get(url,headers=self.headers).text
            yield html
            
    def getsubHtml(self,url):
        r = requests.get(url,headers=self.headers)
        soup = bs(r.text, "html.parser")
        summ = ''.join(soup.find('span',property="v:summary").text.split())
        return summ
    
    def getshort(self,link):
        lst=[]
        for i in range(5):
            kv = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
            url = link+'comments?start={}&limit=20&status=P&sort=new_score'.format(i*20)
            r = requests.get(url, headers = kv)
            soup = bs(r.text, "html.parser")
            for sp in soup.find_all('div',class_="comment"):
                short = sp.find('span',class_="short").text.replace('\n','').replace('\r','')
                if re.findall(r'star\d{1}0', str(sp)):
                    star = re.findall(r'star\d{1}0', str(sp))[0][-2]
                else: 
                    star=None
                lst.append([short,star])
        return str(lst)
##    电影数据提取
            
    def getData(self):
        lst=[]
        gh = self.getHtml() # html源码生成器
        for html in gh: # html:网页源码
            soup = bs(html, 'lxml')
            for info in tqdm(soup.find_all('div', class_='info')):
                c_name = info.find('span',class_='title').text.strip() # 电影中文名
                try:
                    e_name = info.find_all('span',class_='title')[1].text[3:]
                except:
                    e_name = 'None'
                message = info.select('div.bd p')[0].text.strip() #导演、主演、年份、地区信息
                yat = re.search('[0-9]+.*\/?', message).group().split('/') #年份、地区、类型
                year,area,typ = yat[0][:4],yat[1],yat[2]#得到年份、地区、类型
                da = re.search('导演.+\s',message).group().strip()+'...' 
                director = re.findall('导演:(.+?)\s',da)[0].strip() #导演
                link = info.find('a')['href']
                try:
                    summary = self.getsubHtml(link)
                except:
                    summary = '无简介'
                
                #没有主演信息时,进行异常处理
                # try:
                #     mainActors = re.findall('主演:(.+?)[.,]+',da)[0].strip()
                # except IndexError:
                #     mainActors = '暂无主演信息'
                mark_info = info.find('div',class_='star') 
                score= mark_info.find('span',class_='rating_num').text.strip()#评分
                count = re.search('[0-9]+',mark_info.select('span')[3].text).group() #评价人数
                short = self.getshort(link)
                
                #没有简介时,进行异常处理
                try:
                    quote = info.select('p.quote span')[0].text.strip()
                except IndexError:
                    quote = '无概述'
                lst.append([c_name,e_name,link,year,area,typ,director,score,count,quote,summary,short])
        return lst

##  保存到excel文件
    
    def saveToExcel(self,file_name):
        wb = workbook.Workbook()  # 创建Excel对象
        ws = wb.active  # 获取当前正在操作的表对象
        ws.append(['电影中文名','电影英文名','链接', '年份', '地区', '剧情类型', '导演', '评分', '评论人数', '概述', '简介', '短评'])
        gd = self.getData() #数据生成器
        for data in gd:
            ws.append(data)
        wb.save(file_name)
        
    def saveTocsv(self,file_name):
        name = ['电影中文名','电影英文名','链接', '年份', '地区', '剧情类型', '导演', '评分', '评论人数', '概述', '简介', '短评']
        lst = self.getData()
        test = pd.DataFrame(columns=name,data=lst)
        test.to_csv(file_name,index=False)

if __name__ == '__main__':
    start = time.time()
    top = Top250()
    try:
        top.saveTocsv('top250.csv')
        print('抓取成功,用时%4.2f'%(time.time()-start)+'秒')
    except Exception as e:
        print('抓取失败,原因:%s'%e)

