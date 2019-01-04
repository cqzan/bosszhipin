#coding=utf-8
'''
Created by
    author: cq.zan
    time:   2018-12-28
'''

import pandas as pd
import jieba.analyse

df=pd.read_csv("D:/bosszhipin.csv",encoding='gb18030')
dp=df["职位描述"]
string=''
for i in dp:
    string+=i
#因为职位描述栏目下面的文字是没有经过任何处理的，这就需要把代码多运行几遍，把那些没意义词找出来加入停用词表。
jieba.analyse.set_stop_words("D:/tyc.txt")
tags=jieba.analyse.extract_tags(string,topK=100,withWeight=True)
for i in tags:
    print(i[0],int(i[1]*10000))
#打印出来的结果直接在这个网址可以生成云图https://wordart.com/






