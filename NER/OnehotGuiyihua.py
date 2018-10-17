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
def max(a,b):
    if(a>b) :
        return a
    return b
def distance(s1,s2):
    distance = jellyfish.levenshtein_distance(s1, s2)
    similarity = 1-(distance*1.0)/max(len(s1),len(s2))
    return similarity
def guiyihua(corpus):
    length=len(corpus)
    for i in range(len(corpus[0])):
        MAX=-1
        for j in range(length):
            MAX=max(MAX,corpus[j][i])
        for j in range(length):
            MAX = max(MAX, corpus[j][i])
        for j in range(length):
            corpus[j][i]/=MAX
    return corpus
def _calculate(corpus):
    corpus=guiyihua(corpus)
    n=len(corpus)
    m=len(corpus[0])
    A=np.asarray(corpus[0])
    B=np.asarray(corpus[1:n])
    A=A.reshape(1,m)
    B=B.transpose()
    sims = np.dot(A,B)
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
    return ret.split("\t")


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
def getvector(s,res):
    ret=[]
    for word in s:
        if res.get(word) is not None:
            ret.append(int(res[word]))
        else:
            ret.append(int(0))
    return ret
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
                    if (allMention.get(res) is not None):

                        #统计所有title的关键词出现的次数，以及所有title的关键词的集合
                        allword=set()
                        wordnum={}
                        for title in allMention[res]:
                            if (allMentionAbs.get(res) is None or allMentionAbs[res].get(title) is None):
                                continue
                            word_line=change(allMentionAbs[res][title])#所有单词的
                            if (wordnum.get(title) is None):
                                wordnum[title]={}
                            for word in word_line:
                                if(wordnum[title].get(word) is None):
                                    wordnum[title][word]=0
                                wordnum[title][word]+=1#title的关键词出现的次数
                                allword.add(word)
                        if (wordnum.get(res) is None):
                            wordnum[res] = {}
                        word_line = mention
                        for word in word_line:
                            allword.add(word)
                        D = {}  # 需要单独计算
                        for word in word_line:
                            if D.get(word) is None :
                                D[word]=0
                            D[word]+=1
                        candidate.append(getvector(allword,D))
                        for title in allMention[res]:
                            if(allMentionAbs.get(res) is None or allMentionAbs[res].get(title) is None) :
                                continue
                            candidate.append(getvector(allword,wordnum[title]))
                            candidatetitle.append(title)
                        if(len(candidatetitle)):
                            queue.append(candidatetitle[_calculate(candidate)])
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