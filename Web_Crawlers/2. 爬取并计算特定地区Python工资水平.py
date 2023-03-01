##爬取了猎聘网站上，特定地区的工资分布。Python有多吃香一看便知

import time
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

class JobSpider:
  # 初始化方法
  def __init__(self):
    self.session = requests.Session()
    self.headers = {
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    }
    self.session.headers.update(self.headers)

  # 获取数据方法
  def get_data(self):
    # 用列表存储多条招聘信息
    data = []
    for i in range(10):
      params = {
        "key": "python",  # 搜索关键字
        "dqs": "020",  # dqs 值为 020 代表上海
        "init": "-1",
        "searchType": "1",
        "headckid": "53ec9ad5e94c5aa3",
        "fromSearchBtn": "2",
        "sortFlag": "15",
        "ckid": "53ec9ad5e94c5aa3",
        "degradeFlag": "0",
        "siTag": "I-7rQ0e90mv8a37po7dV3Q~fA9rXquZc5IkJpXC-Ycixw",
        "d_sfrom": "search_prime",
        "d_ckId": "d3f6ab254ea9709019f07af9463d4ebe",
        "d_curPage": str(i - 1),  # 前一页页码数
        "d_pageSize": "40",  # 每页数据条数
        "d_headId": "d3f6ab254ea9709019f07af9463d4ebe",
        "curPage": str(i)  # 当前页页码数
      }
      req = self.session.get('https://www.liepin.com/zhaopin/', params=params)

      if req.status_code == 200:
        print('第{}页数据获取成功'.format(i + 1))
        soup = BeautifulSoup(req.text, 'html.parser')
        job_items = soup.find_all('div', class_='sojob-item-main')

        for item in job_items:
          # 职位信息
          job_info = item.find('div', class_='job-info')
          job_name = job_info.find('h3')['title'][2:]
          conditions = job_info.find('p', class_='condition')['title']
          conditions_list = conditions.split('_')
          salary = conditions_list[0]
          area = conditions_list[1]
          edu_level = conditions_list[2]
          working_exp = conditions_list[3]
          # 公司信息
          company_info = item.find('div', class_='company-info')
          company_name = company_info.find('p', class_='company-name').find('a').text
          company_type = company_info.find('p', class_='field-financing').text.strip()

          # 用字典存储每条招聘信息
          result = {
            'job_name': job_name,
            'salary': salary,
            'area': area,
            'edu_level': edu_level,
            'working_exp': working_exp,
            'company_name': company_name,
            'company_type': company_type
          }
          # 将每条招聘信息存到列表中
          data.append(result)
      else:
        print('第{}页数据获取失败'.format(i + 1))
      time.sleep(1)
    return data

  # 处理数据方法
  def process_data(self):
    data = self.get_data()
    total = 0
    count = 0
    # 表格数据
    rows = [['公司名', '公司类型', '地区', '职位', '薪资', '平均薪资', '学历要求', '经验要求']]

    for item in data:
      company_name = item['company_name']
      company_type = item['company_type']
      area = item['area']
      job_name = item['job_name']
      salary = item['salary']
      edu_level = item['edu_level']
      working_exp = item['working_exp']

      if salary != '面议':
        salary_range, salary_times_str = salary.split('k·')  # 分割成两部分
        if '-' in salary_range:
          salary_min_str, salary_max_str = salary_range.split('-')  # 分割薪资范围
          salary_min = int(salary_min_str) * 1000  # 最低月薪
          salary_max = int(salary_max_str) * 1000  # 最高月薪
          salary_value = (salary_min + salary_max) / 2 # 平均月薪
        else:
          salary_value = int(salary_range) * 1000 # 平均月薪
        salary_times = int(salary_times_str.replace('薪', ''))  # 一年发多少薪
        salary_avg = salary_value * salary_times  # 计算平均年薪
        total += salary_avg
        count += 1
      else:
        salary_avg = '面议'
      # 按公司名，公司类型，地区，职位，薪资，平均薪资，学历要求，经验要求排列
      row = [company_name, company_type, area, job_name, salary, salary_avg, edu_level, working_exp]
      rows.append(row)
    print('上海地区 Python 的平均年薪是{}元'.format(total / count))
    return rows

  # 保存数据方法
  def save_data(self):
    # 处理后的数据
    rows = self.process_data()
    # 新建工作簿
    wb = Workbook()
    # 选择默认的工作表
    sheet = wb.active
    # 给工作表重命名
    sheet.title = 'python职位信息'
    # 将数据一行一行写入
    for row in rows:
      sheet.append(row)

    # 保存文件
    wb.save('猎聘职位信息表.xlsx')

spider = JobSpider()
spider.save_data()