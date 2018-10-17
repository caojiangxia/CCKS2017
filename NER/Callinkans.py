#coding=utf-8
import threadpool
import urllib.request
import urllib.response
from urllib.parse import quote
import re
import pickle

se=set()
se2=set()
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
        se.clear()
        se2.clear()
        for i in range(len(line[0])):
            res=line[0][i].strip()+line[1][i].strip()
            se.add(res)
        for i in range(len(line2[0])):
            res=line2[0][i].strip()+line2[1][i].strip()
            se2.add(res)
        cntA+=len(se)
        cntC += len(se&se2)
        cntB += len(se2)
    f2.close()
    f.close()
    print(str(cntA) + " " + str(cntB) + " " + str(cntC))
    print("精确率=" + str(float(cntC / cntA)))
    print("召回率=" + str(float(cntC / cntB)))
    print("F1=" + str(float(cntC / cntB) * float(cntC / cntA) / (float(cntC / cntB) + float(cntC / cntA))))
if __name__ == '__main__':
    cal("标准输出.txt","Link_ans.txt")