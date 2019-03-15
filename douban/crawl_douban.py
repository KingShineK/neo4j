# -*- coding: utf-8 -*-
import requests
import csv
import pandas as pd
import re
from bs4 import BeautifulSoup

df = pd.read_csv('url.csv', encoding='utf-8')
urls = df['url']
header = {
        'Host': 'movie.douban.com',
        'Origin': "movie.douban.com",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    }
# 用来存储爬取的数据
results = []
i = 1
for url in urls:
    response = requests.post(url, headers=header)
    response.encoding = 'utf-8'

    # data去除html标签
    reg_data = re.compile(r'<[^>]+>', re.S)

    soup = BeautifulSoup(response.content,'lxml')
    film = soup.find_all('h1')[0].find_all('span',property='v:itemreviewed')
    film = reg_data.sub('', str(film[0])).split()[0]

    x = soup.find_all('div',id='info')[0]
    try:
        director = x.find_all('span')[0].find_all('span',class_='attrs')
        actor = x.find_all('span',class_='actor')[0].find_all('span',class_='attrs')
        type = x.find_all('span',property = 'v:genre')

        director = reg_data.sub('',str(director[0])).replace(' ','')
        actor = reg_data.sub('',str(actor[0])).replace(' ','')
        res = ''
        for t in type:
            res = res + reg_data.sub('', str(t)) + '/'
        type = res.rstrip('/').replace(' ','')

    except:
        print('第%d条爬取出现错误' % i )
        continue
    else:
        result = [film, director, actor, type]
        results.append(result)
        print('第%d条爬取成功' % i)
    i += 1

print('数据开始导出到CSV')
# 将总数据转化为data frame再输出
df = pd.DataFrame(data=results, columns=['电影名称', '导演', '演员', '类型'])
df.to_csv('douban.csv', index=False, encoding='utf-8_sig')
print('数据导出到CSV成功')

