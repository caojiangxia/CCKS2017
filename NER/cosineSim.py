# # -*- coding: utf-8 -*-
# """
# Created on Mon Jun 26 15:28:49 2017
#
# @author: ethel
# """
#
# import os
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.feature_extraction.text import TfidfTransformer
# from sklearn.metrics.pairwise import cosine_similarity
# import pickle
#
# stpwrdpath = 'stopwords.dat'
# #导入停用词
# stpwrd_dic = open(stpwrdpath, 'rb')
# stpwrd_content = stpwrd_dic.read()
# stpwrdlst = stpwrd_content.splitlines()
# stpwrd_dic.close()
# allMentionInf={}
# def _calculateCos(corpus):
#     # corpus=["3点\t我了\t来到\t北京\t北京大学",#第一类文本(比如mention)切词后的结果，词之间以\t隔开
#     #     "我\t来到\t了\t网易\t杭研\t大厦\t北京大学",#第二类文本的切词结果
#     #     "小明\t硕士\t毕业\t与\t中国\t科学院",#第三类文本的切词结果
#     #     "我\t爱\t北京\t天安门"]#第四类文本的切词结果
#     vectorizer = CountVectorizer(stop_words=stpwrdlst)#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
#     transformer = TfidfTransformer()#该类会统计每个词语的tf-idf权值
#     tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
#     sims = cosine_similarity(tfidf[0:1],tfidf)[:,1:len(corpus)]
#     word=vectorizer.get_feature_names()#获取词袋模型中的所有词语
# #print word
#     weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
#     for i in range(len(weight)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for遍历某一类文本下的词语权重
#         print(u"-------这里输出第",i,u"类文本的词语tf-idf权重------")
#         for j in range(len(word)):
#             print(word[j],weight[i][j])
#
# #print similarity
#     maxsim = sims.max(axis=1)[0]
#     maxidx = sims.argmax(axis=1)[0]
#     print('mention与每一个title的相似度：',sims)
#     print('最相似title的id号：',maxidx)
#     print('最相似title的相似度：',maxsim)
#     return int(maxidx)
# def judge(line):
#     if(line.startswith("n")) :
#         return 1
#     if (line.startswith("v")):
#         return 1
#     return 0
#
# def change(line):
#     res=line.split()
#     ret=""
#     for i in range(len(res)):
#         ok = 0
#         pre=""
#         suf=""
#         for j in range(len(res[i])):
#             if(res[i][j]=='[' or res[i][j]=="]"):
#                 continue
#             if(res[i][j]=="/" or res[i][j]==" " or res[i][j]=="\n"):
#                 ok+=1
#                 if(ok<2) :
#                     continue
#             if(ok==0):
#                 pre+=res[i][j]
#             elif(ok==1):
#                 suf+=res[i][j]
#             else:
#                 break
#         if(judge(suf)):
#             if(len(ret)):
#                 ret+="\t"
#             ret+=pre
#     return ret
# def Init_text(fenci,ans2):
#     fr = open(fenci, "r", encoding="utf-8")
#     f = open(ans2, "r")
#     out = open("Init_for_link.txt", "w")
#     ok = 0
#     for line in fr:
#         if (ok == 0):
#             ok = 1
#         else:
#             ok = 0
#             line2 = f.readline()
#             line = change(line)
#             out.write(line + " " + line2)
#     out.close()
#     f.close()
#     fr.close()
# def get_Mentiontitle(name):
#     fr = open(name, "r", encoding="utf-8")
#     mention = title = inf = ""
#     for line in fr:
#         if (mention == ""):
#             mention = line
#             continue
#         if (title == ""):
#             title = line
#             continue
#         inf = line
#         mention = mention[0:len(mention) - 1]
#         title = title[0:len(title) - 1]
#         inf = inf[0:len(inf) - 1]
#         if (allMentionInf.get(mention) is None):
#             allMentionInf[mention] = {}
#             allMentionInf[mention][title] = ""
#         allMentionInf[mention][title] = inf
#         mention = title = inf = ""
#     fr.close()
# def get_ans(name):
#     fr=open(name,"r")
#     fw = open("第三列2", "w")
#     candidate=[]
#     candidatetitle=[]
#     queue=[]
#     res=""
#     mention=""
#     for line in fr:
#         ok=0
#         for i in range(len(line)):
#             if(line[i]==' '):
#                 mention=res
#                 res=""
#                 ok=1
#                 continue
#             if(ok==0):
#                 res+=line[i]
#             else:
#                 if(line[i]=='|'):
#                     if(len(res)==0):
#                         continue
#                     else:
#                         candidatetitle.clear()
#                         candidate.clear()
#                         candidate.append(mention)
#                         if(allMentionInf.get(res) is not None):
#                             for title in allMentionInf[res]:
#                                 candidate.append(change(allMentionInf[res][title]))
#                                 candidatetitle.append(title)
#                             queue.append(candidatetitle[_calculateCos(candidate)])
#                         else :
#                             queue.append("nil")
#                         res=""
#                 else :
#                     res+=line[i]
#         fw.write("|||".join(queue))
#     fw.close()
#     fr.close()
#
# if __name__ == '__main__':
#     #_calculateCos()
#     # fr = open('allMentionTag.pkl', 'rb')
#     # allMentionInf = pickle.load(fr)
#     # fr.close()
#     Init_text("分词结果.txt","第二列2.txt")
#     get_Mentiontitle("MentionTitleInfdiv.txt")
#     get_ans("Init_for_link.txt")
#
#
#
# #****************************
# '''
# 切记
# MentionTitleInfdiv 这个文件是存infbox的划分结果的
# 每个样例三列
# mention
# title
# 细粒度infbox
#
# get_ans之前我们需要初始化Init_for_link文件
# 这个文件存储的信息是细粒度的n,v,之类的词，后面跟着实体划分结果
# 在此之前还需要准备一个文件，存的是分词结果和我们所找到的实体
#
#
#
# 最后的queue则是划分最终结果
# '''





# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 15:28:49 2017

@author: ethel
"""

import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import jellyfish
import numpy as np

stpwrdpath = 'stopwords.dat'
# 导入停用词
stpwrd_dic = open(stpwrdpath, 'rb')
stpwrd_content = stpwrd_dic.read()
stpwrdlst = stpwrd_content.splitlines()
stpwrd_dic.close()
allMention={}
allMentionAbs={}
setns=set()
setnt=set()
setnr=set()
se = set()
dic={}

def distance(s1,s2):
    distance = jellyfish.levenshtein_distance(s1, s2)
    similarity = 1-(distance*1.0)/max(len(s1),len(s2))
    return similarity

def _calculateCos(corpus):
    # corpus=["3点\t我了\t来到\t北京\t北京大学",#第一类文本(比如mention)切词后的结果，词之间以\t隔开
    #     "我\t来到\t了\t网易\t杭研\t大厦\t北京大学",#第二类文本的切词结果
    #     "小明\t硕士\t毕业\t与\t中国\t科学院",#第三类文本的切词结果
    #     "我\t爱\t北京\t天安门"]#第四类文本的切词结果
    vectorizer = CountVectorizer(stop_words=stpwrdlst)  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(
        vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    sims = cosine_similarity(tfidf[0:1], tfidf)[:, 1:len(corpus)]
    #print sims.shape , weight.shape
    #weight.reshape(1,7)
    #score =  np.argmax(weight * sims, axis=1)
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    # print word
    # weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    # for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for遍历某一类文本下的词语权重
    #     print(u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
    #     for j in range(len(word)):
    #         print(word[j], weight[i][j])

    # print similarity
    maxsim =sims.max(axis=1)[0]
    maxidx = sims.argmax(axis=1)[0]
    # print('mention与每一个title的相似度：', sims)
    # print('最相似title的id号：', maxidx)
    # print('最相似title的相似度：', maxsim)
    return int(maxidx)

def judge(line):
    if (line.startswith("n")):
        return 1
    if (line.startswith("v")):
        return 1
    return 0

def change(line):
    res = line.split()
    ret = ""
    for i in range(len(res)):
        ok = 0
        pre = ""
        suf = ""
        for j in range(len(res[i])):
            if (res[i][j] == '[' or res[i][j] == "]"):
                continue
            if (res[i][j] == "/" or res[i][j] == " " or res[i][j] == "\n"):
                ok += 1
                if (ok < 2):
                    continue
            if (ok == 0):
                pre += res[i][j]
            elif (ok == 1):
                suf += res[i][j]
            else:
                break
        if (judge(suf)):
            if (len(ret)):
                ret += "\t"
            ret += pre
    return ret


def Init_text(fenci, ans2):
    fr = open(fenci, "r", encoding="utf-8")
    f = open(ans2, "r")
    out = open("Init_for_link.txt", "w")
    ok = 0
    for line in fr:
        if (ok == 0):
            ok = 1
        else:
            ok = 0
            line2 = f.readline()
            line=line.strip()
            out.write(line + "#" + line2)
    out.close()
    f.close()
    fr.close()


def get_abstract(name):
    fr = open(name, "r", encoding="utf-8")
    mention = title = inf = ""
    for line in fr:
        if (mention == ""):
            mention = line
            continue
        if (title == ""):
            title = line
            continue
        inf = line
        mention = mention.strip()
        title = title.strip()
        inf = inf.strip()
        if (allMentionAbs.get(mention) is None):
            allMentionAbs[mention] = {}
        allMentionAbs[mention][title] = inf
        mention = title = inf = ""
    fr.close()

def get_ans(name):
    fr = open(name, "r")
    fw = open("第三列2.txt", "w")
    candidate = []
    candidatetitle = []
    queue = []
    enti=[]
    res = ""
    mention = ""
    id=0
    for line in fr:
        ok = 0
        id+=1
        queue.clear()
        enti.clear()
        for i in range(len(line)):
            if (line[i] == '#'):
                mention = change(res)
                res = ""
                ok = 1
                continue
            if (ok == 0):
                res += line[i]
            else:
                if (line[i] == '|' or line[i]=="\n"):
                    if (len(res) == 0):
                        continue
                    candidatetitle.clear()
                    candidate.clear()
                    candidate.append(mention)
                    if (allMention.get(res) is not None):
                        for title in allMention[res]:
                            if(allMentionAbs.get(res) is None or allMentionAbs[res].get(title) is None) :
                                continue
                            candidate.append(change(allMentionAbs[res][title]))
                            candidatetitle.append(title)
                        if(len(candidatetitle)):
                            queue.append(candidatetitle[_calculateCos(candidate)])
                        else :
                            queue.append("nil")
                    else:
                        queue.append("nil")
                    enti.append(res)
                    res = ""
                else:
                    res += line[i]
        line.strip()
        fw.write("|||".join(enti)+"\t"+"|||".join(queue)+"\n")
    fw.close()
    fr.close()

def suf(pos,str):
    res=""
    while(pos<len(str)):
        if(str[pos]>='a' and str[pos]<='z'):
            res=res+str[pos]
        else: return res;
        pos+=1
    return res
def load_date(name):
    f = open(name, 'r', encoding='utf-8')
    for line in f:
        for res in line.split():
            ans = ""
            for i in range(len(res)):
                if (res[i] == '['):
                    continue
                elif(res[i]=='/'):
                    if (len(ans) > 1 and ans not in se):
                        se.add(ans)
                        dic[ans]=suf(i+1,res)
                    break
                else :
                    ans=ans+res[i]
    f.close()

def div_to_excle(ans,A,B,C):  #     ans-细粒度，A-正确答案的实体链接，B-我们的实体，C-我们的实体链接。
    f = open(ans, "r",encoding="utf-8")
    f2 = open(A, "r")
    f3 = open(B, "r")
    f4 = open(C, "r")
    out=open("实体链接划分结果.txt","w")
    for line2 in f2:
        line=f.readline()
        line=f.readline()
        line3=f3.readline()
        line4 = f4.readline()
        line=line[0:len(line)-1]
        line2=line2.strip()
        line3 = line3[0:len(line3) - 1]
        line4 = line4[0:len(line4) - 1]
        out.write(line+"*****"+line2+"*****"+line4+"\n")
    out.close()
    f4.close()
    f3.close()
    f2.close()
    f.close()


see=set()
see2=set()
def cal(standard,test):
    f = open(standard,"r")
    f2 = open(test, "r")
    cntA=cntB=cntC=0
    for line in f:
        line2=f2.readline()
        line=line.strip()
        line2 = line2.strip()
        line=line.split("\t")
        line2 = line2.split("\t")
        line[0]=line[0].split("|||")
        if(len(line)==2):
            line[1] = line[1].split("|||")
        line2[0] = line2[0].split("|||")
        if (len(line2) == 2):
            line2[1] = line2[1].split("|||")
        see.clear()
        see2.clear()
        if(len(line)>1):
            for i in range(len(line[0])):
                res=line[0][i]+line[1][i]
                see.add(res)
        if (len(line2) > 1):
            for i in range(len(line2[0])):
                res=line2[0][i]+line2[1][i]
                see2.add(res)
        cntA+=len(see)
        cntC += len(see&see2)
        cntB += len(see2)
    f2.close()
    f.close()
    print(str(cntA) + " " + str(cntB) + " " + str(cntC))
    print("精确率=" + str(float(cntC / cntB)))
    print("召回率=" + str(float(cntC / cntA)))
    print("F1=" + str(2*float(cntC / cntB) * float(cntC / cntA) / (float(cntC / cntB) + float(cntC / cntA))))


if __name__ == '__main__':
    load_date("分词结果.txt")  #词性字典
    fr = open('allMentionTag.pkl', 'rb')
    allMention = pickle.load(fr)
    fr.close()
    Init_text("分词结果.txt", "第二列2.txt")
    #Init_text("分词结果_test.txt", "第二列_test.txt")
    get_abstract("AbstractDiv.txt")
    get_ans("Init_for_link.txt")
    cal("标准输出.txt","第三列2.txt")
    div_to_excle("分词结果.txt","标准输出.txt","第二列2.txt","第三列2.txt")

# ****************************
'''
切记
AbstractDiv.txt 这个文件是存abstract的划分结果的
每个样例三列
mention
title
细粒度abstract

get_ans之前我们需要初始化Init_for_link文件
这个文件存储的信息是细粒度的n,v,之类的词，后面跟着实体划分结果
在此之前还需要准备一个文件，存的是分词结果和我们所找到的实体



最后的queue则是划分最终结果
'''