#coding=utf-8
import urllib.request
import urllib.response
from urllib.parse import quote
import re
import pickle
countns={}
countnt={}
countnr={}
allMentionTag={}
def max(a,b):
    if(a>b) :
        return a
    return b
def min(a,b):
    if(a>b) :
        return b
    return a
def find(line,res):
    j=0
    i=0
    for i in range(len(line)):
        for j in range(i,min(len(line),i+len(res))):
            if(line[j]==res[j-i]):
                continue
            break
        j+=1
        if(j==i+len(res) and(j==len(line) or line[j]=="/")):
            break
    if(i+1==len(line)):
        return ""
    j+=1
    res=""
    while j<len(line) and line[j]!="/" and line[j]!=" " and line[j]!="\n":
        if(line[j]=="]"):
            j+=1
            continue
        res+=line[j]
        j+=1
    return res
def lineget(line,cnt):
    ret=[]
    res=""
    for i in range(len(line)):
        if(cnt==-1) :
            return  ret
        if(line[i]=="|" or line[i]=="\t" or line[i]=="\n"):
            if(len(res) and cnt==0):
                ret.append(res)
            res=""
            if(line[i]=="\t"):
                cnt-=1
            continue
        res+=line[i]
    return  ret
def add(count,res1,res2):
    if ((allMentionTag.get(res1) is not None) and (allMentionTag[res1].get(res2) is not None)):
        for type in allMentionTag[res1][res2]["type"]:
            if (count.get(type) is None):
                count[type] = 0
            count[type] += 1
def CountType(fr,fr2):
    for line in fr:
        line2 = fr2.readline()
        line2 = fr2.readline()
        if(len(line)==0):
            continue
        res1 = lineget(line,int(0))
        res2 = lineget(line,int(1))
        for i in range(len(res1)):
            if(res2[i]=="nil"):
                continue
            res=res1[i][max(0,len(res1)-2):len(res1)]
            res=find(line2,res)
            if(res.startswith("ns")):
                add(countns,res1[i],res2[i])
            if (res.startswith("nt")):
                add(countnt, res1[i], res2[i])
            if (res.startswith("nr")):
                add(countnr, res1[i], res2[i])
if __name__ == '__main__':
    allMentionTag.clear()
    fr = open('allMentionTag.pkl', 'rb')
    allMentionTag = pickle.load(fr)
    fr.close()
    fr=open("标准输出.txt","r")
    fr2 = open("分词结果.txt", "r",encoding="utf-8")
    CountType(fr,fr2)
    fr2.close()
    fr.close()
    countns = sorted(countns.items(), key=lambda d: d[1], reverse=True)
    countnt = sorted(countnt.items(), key=lambda d: d[1], reverse=True)
    countnr = sorted(countnr.items(), key=lambda d: d[1], reverse=True)
    print("startswith ns")
    print(countns)
    print("startswith nt")
    print(countnt)
    print("startswith nr")
    print(countnr)
