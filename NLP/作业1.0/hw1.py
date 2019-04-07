import re
import collections
import numpy as np
import jieba
from jieba import analyse
import pandas as pd
import operator
import codecs
txt=[]#分词在每篇的总表，二维列表
new_txt=[]  #去除了停用词的二维列表
alllist=[]  #合并txt并转为set
stopwords = [line.strip() for line in codecs.open(r'stoped.txt', 'r').readlines()] #导入停用词表

#打开文本并预处理
for i in range(3):
    
    file=open(r"txt"+format(i+1)+".txt")#打开文章
    txt.append(file.read())
    file.close()
    re.sub("\\u3000|\\t|\\n|",'',txt[i]) #正则预处理
    txt[i]=jieba.lcut(txt[i],cut_all=False)#精确模式分词
    temp=[]#临时存放去除停用后的词
    
    for word in txt[i]:#去除停用词
        if word  not in stopwords:
            temp.append(word)
    new_txt.append(temp)  #添加到二维列表
    alllist.extend(txt[i])

alllist=set(alllist)  #将总词和符号转为set 要在转为字典之前
corpus_dict = dict(zip(alllist, range(len(alllist))))  #将词和符映射为数字
def vector_rep(text, corpus_dict):  
    vec = []
    for key in corpus_dict.keys():#遍历一遍所有的分词
        if key in text:  #在文本里有就利用conut数出
            vec.append((corpus_dict[key], text.count(key)))
        else:  #没有就是0
             vec.append((corpus_dict[key], 0))

    vec = sorted(vec, key= lambda x: x[0])   #以键大小排序
    for i in range (len(vec)):
        vec[i]=vec[i][1]
    return vec#去掉前缀

vec1 = vector_rep(new_txt[0], corpus_dict)
vec2 = vector_rep(new_txt[1], corpus_dict)
vec3 = vector_rep(new_txt[2], corpus_dict)

alll=[vec1,vec2,vec3]
cout=0
 #打印分词
print(alllist)
for i in alll:  #打印向量
    cout+=1
    print("NO."+format(cout)+"\n")
    print(i)
    print("*"*50)


