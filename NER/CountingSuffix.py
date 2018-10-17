#coding=utf-8
import urllib.request
import urllib.response
from urllib.parse import quote
import re
import pickle
count={}
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
def CountSuffix(fr,fr2):
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
            if(len(res) and count.get(res) is None):
                count[res]=0
            if(len(res)):
                count[res]+=1
if __name__ == '__main__':
    fr=open("标准输出.txt","r")
    fr2 = open("分词结果.txt", "r",encoding="utf-8")
    CountSuffix(fr,fr2)
    fr2.close()
    fr.close()
    count = sorted(count.items(), key=lambda d: d[1], reverse=True)
    print(count)
