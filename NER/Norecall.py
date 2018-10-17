#coding=utf-8
import threadpool
import urllib.request
import urllib.response
from urllib.parse import quote
import re
import pickle
'''
#这一部分代码是用来将我们的初步结果和训练数据的结果进行对比，得到精确率和召回率
注意的地方：
1.第一个参数为初步结果的文件名，第二个参数才是训练数据的名字
'''

def get_ans(test,name):
    #f=open(test,"r",encoding="utf-8")
    #f2=open(name,"r",encoding="utf-8")
    f = open(test, "r")
    f2=open(name,"r")
    s=set()
    s2=set()
    cntA=cntB=cntC=0
    for line in f:
        line2=f2.readline()
        s.clear()
        s2.clear()
        L=-1
        for i in range(len(line)):
            if(line[i]=="\n"):
                res = line[L:i]
                if (L != -1): s.add(res)
            elif(line[i]=='|'):
                if(L!=-1):
                    res=line[L:i]
                    s.add(res)
                    L=-1
            else :
                if(L==-1):L=i
        L=-1
        for i in range(len(line2)):
            if(line2[i]=='\t'):
                if (L != -1): s2.add(line2[L:i])
                break
            elif(line2[i]=='|'):
               if(L!=-1):
                    res=line2[L:i]
                    s2.add(res)
                    L=-1
            else :
                if(L==-1):L=i
        cntA+=len(s)
        cntB += len(s2)
        cntC+=len(s&s2)
    print(str(cntA)+" "+str(cntB)+" "+str(cntC))
    print("精确率="+str(float(cntC/cntA)))
    print("召回率=" + str(float(cntC / cntB)))
    print("F1=" + str(float(cntC / cntB)*float(cntC / cntA)/(float(cntC / cntB)+float(cntC / cntA))))
'''
#这一部分代码是用来将SWJTU的分词用上一步爬取的重定向结果进行词性分析.得到第二列和第三列的初步结果
注意的地方：
1.有两个文件需要进行处理得到实体
2.judge函数可以进行修改
3.由于逻辑层次相对复杂一点，调试时务必小心
4.输出文档按照gbk编码
5.这个版本是驱虎汉语词汇且没有召回的。

1544 1966 735
精确率=0.47603626943005184
召回率=0.3738555442522889
F1=0.20940170940170938
#***************************************************************************
'''
enti=set()
YES=0
allMentionTag={}
def judge(str):
    if(str.startswith("nr") or str.startswith("ns") or str.startswith("nf") or str.startswith("nn") or str.startswith("nm") or str.startswith("nb") or str.startswith("nh") or str=="j"):
        return 1
    elif(str.startswith("nt") or str.startswith("nz") or str=="l" or str=="n"):
        return 2
    else:
        return 0
def in_(res):
    if(allMentionTag.get(res)):
        if(len(allMentionTag[res])>0):
            return 1
    return 0
def not_have(all):
    for title in all:
        if(all[title].get("tag") is not None):
            if("词语概念" in all[title]["tag"]) :
                return 0
            if ("汉语词汇" in all[title]["tag"]):
                return 0
            if ("汉语词语" in all[title]["tag"]):
                return 0
            if ("字词" in all[title]["tag"]):
                return 0
            if ("词汇" in all[title]["tag"]):
                return 0
            if ("词语" in all[title]["tag"]):#可以影响十个点
                return 0
            if ("语言" in all[title]["tag"]):
                return 0
            if ("字" in all[title]["tag"]):
                return 0
            if ("词" in all[title]["tag"]):
                return 0
    return 1
def do_(ans,pos,ok):
    global enti,YES,allMentionTag
    ook=-1
    if(pos>=len(ans)):
        return pos
    if(ans[pos][0]=='['):
        if(ok==2):
            ok=3
        else :
            ok=4
        ans[pos]=ans[pos][1:len(ans[pos])]
    elif(ans[pos+1][len(ans[pos+1])-1]==']'):
        ook=0
        ans[pos+1] = ans[pos+1][0:len(ans[pos+1])-1]
    elif (ok == 1 or ok == 2):
        ook = 0
    jud=judge(ans[pos+1])
    if(len(ans[pos])<2):
        q=0
    elif(ok==3):
        if(in_(ans[pos])):
            if(not_have(allMentionTag[ans[pos]])):
                enti.add(ans[pos])
    elif(ok==1) :
        if(jud==1):
            YES=1
            if(len(enti)!=0):
                enti.add(ans[pos])
        elif(jud==2):
            if(in_(ans[pos])):
                if(not_have(allMentionTag[ans[pos]])):
                    enti.add(ans[pos])
                    YES = 1
    pos+=2
    if(ook!=-1):
        ok=ook
    if(ok) :
        return do_(ans,pos,ok)
    else :
        return pos

def gao(dat,DAT):
    global enti,YES
    ans=[]
    ANS = []
    enti.clear()
    ok=0
    for i in range(len(dat)):
        t=dat[i].split("/")
        for j in range(len(t)):
            ans.append(t[j])
    for i in range(len(DAT)):
        t = DAT[i].split("/")
        for j in range(len(t)):
            if (ok == 0):
                if (len(t[j]) == 1 and (t[j][0] == '[' or t[j][0] == ']')):
                    ok = 1
                    continue
                ANS.append(t[j])
            else:
                ok = 0
            if (t[j][len(t[j]) - 1] == ']'):
                ok = 1
    i=0
    j=0
    while(i<len(ans)):
        YES = 0
        i = do_(ans, i, 1)
        if (YES):
            j = do_(ANS, j, 0)
        elif(YES==0):
            j = do_(ANS, j, 2)

def do_date(name):
    global enti
    output=open("第二列2.txt","w")
    f=open(name,"r",encoding="utf-8")
    dat=[]
    DAT=[]
    dat.clear()
    DAT.clear()
    for line in f:
        if(len(dat)==0):
            dat=line.split()
        else :
            DAT=line.split()
            gao(dat,DAT)
            output.write("|||".join(list(enti))+"\n")
            dat.clear()
            DAT.clear()
    f.close()
    output.close()

def div_to_excle(ans,A,B,C):  #     ans-细粒度，A-正确答案，B-baseline，C-combain。
    f = open(ans, "r",encoding="utf-8")
    f2 = open(A, "r")
    f3 = open(B, "r")
    f4 = open(C, "r")
    out=open("去除汉语词汇.txt","w")
    for line2 in f2:
        line=f.readline()
        line=f.readline()
        line3=f3.readline()
        line4 = f4.readline()
        line=line[0:len(line)-1]
        if(len(line2.split())) :
            line2 = line2.split()[0]
        else :
            line2 = ""
        line3 = line3[0:len(line3) - 1]
        line4 = line4[0:len(line4) - 1]
        out.write(line+"\t\t"+line2+"\t"+line3+"\t"+line4+"\n")
    out.close()
    f4.close()
    f3.close()
    f2.close()
    f.close()
if __name__ == '__main__':
    allMentionTag.clear()
    fr = open('allMentionTag.pkl', 'rb')
    allMentionTag = pickle.load(fr)
    fr.close()
    do_date("分词结果.txt")
    get_ans("第二列2.txt", "标准输出.txt")
    #div_to_excle("分词结果.txt", "标准输出.txt", "第二列.txt", "第二列2.txt")
