#coding=utf-8
'''
Created by
    author: cq.zan
    time:   2018-11-20
'''

import requests
from lxml import etree
import pandas as pd
import time
import re
import random
baseurl="https://www.zhipin.com"
url="https://www.zhipin.com/c101280600"
headers={
"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"accept-encoding":"gzip, deflate, sdch, br",
"accept-language":"zh-CN,zh;q=0.8",
"cache-control":"max-age=0",
"cookie":"****",
"upgrade-insecure-requests":"1",
"user-agent":"****",
}

#r=requests.get(url=url, params=param, headers=headers)

#soup_a = BeautifulSoup(r.text, "lxml")
#print(soup_a)

def detail_url(param):
    """
     获取每个职位详情页的url地址
    """
    url_list = []
    html=requests.get(url=url,headers=headers,params=param)
    path_html=etree.HTML(html.text)
    hrefs=path_html.xpath(".//div[@class='info-primary']//a/@href")
    for href in hrefs:
        detail_url=baseurl+href
        url_list.append(detail_url)
    return url_list

def detail_data(html_data):
    """
    从detail_url中，提取想要的信息
    """
    retext = re.compile(r'<br/>|<(em).*?>.*?</\1>')
    #去掉标签中的<br/> 和 <em></em>标签，便于提取
    html_text = retext.sub('', html_data.text)
    path_htmldata=etree.HTML(html_text)
    imfo={}
    # 发布日期/招聘要求/职位名/薪水/公司名称/公司规模/工作职责/地址
    imfo['publishTime'] =path_htmldata.xpath(".//div[@class='info-primary']//span[@class='time']/text()")[0]
    imfo['requirement'] = path_htmldata.xpath("//div[@class='job-banner']//div[@class='info-primary']//p/text()")[0]
    imfo['position'] =path_htmldata.xpath(".//div[@class='info-primary']//h1/text()")[0]
    imfo['salary'] = path_htmldata.xpath(".//div[@class='info-primary']//span[@class='badge']/text()")[0].strip()
    imfo['companyName'] = path_htmldata.xpath("//div[@class='info-company']//h3/a/text()")[0]
    imfo['companySize'] = path_htmldata.xpath("//div[@class='info-company']//p/text()")[0]
    imfo['responsibility'] = path_htmldata.xpath("//div[@class='job-sec']//div[@class='text']/text()")[0].strip()
    imfo["address"]=path_htmldata.xpath("//div[@class='location-address']/text()")[0]
    t=random.randint(3,15)
    time.sleep(t)
    return imfo

def insert_csv(datas):
    """
    将数据写入csv
    """
    df=pd.DataFrame(datas)
    file_name="zp"
    df.to_csv('{}.csv'.format(file_name),mode='a',encoding='utf-8-sig')

if __name__ == "__main__":
    keyword=input("请输入搜索关键词：")
    for page_num in range(1,11):
        param = {
        "query": keyword,
        "page": page_num
         }
        #还有一个参数ka可以忽略
        datas = []
        url_list=detail_url(param)
        for data_url in url_list:
            #print(data_url)
            html_data = requests.get(url=data_url, headers=headers, params=None)
            text=detail_data(html_data)
            datas.append(text)
            print(text)
        insert_csv(datas)
        print(datas)


