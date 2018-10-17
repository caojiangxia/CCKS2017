#coding=utf-8
import threadpool
import urllib.request
import urllib.response
from urllib.parse import quote
import re
import pickle

def get_ans(test,name):
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
    print("F1=" + str(2*float(cntC / cntB)*float(cntC / cntA)/(float(cntC / cntB)+float(cntC / cntA))))
'''
#这一部分代码是用来将SWJTU的分词用上一步爬取的重定向结果进行词性分析.得到第二列和第三列的初步结果
注意的地方：
1.有两个文件需要进行处理得到实体
2.judge函数可以进行修改
3.由于逻辑层次相对复杂一点，调试时务必小心
4.输出文档按照gbk编码
5.这个版本链接了
长度小的不要 x/m+n/nz,nrf/n/nz+x/m,ntc+n,x长度大于2且无匹配时输出

2964 1966 1339
精确率=0.4517543859649123
召回率=0.6810783316378434
F1=0.5432048681541582
#***************************************************************************
'''
enti=set()
YES=0
allMentionTag={}
def judge(str):
    if(str.startswith("nr") or str.startswith("ns") or str.startswith("nf") or str.startswith("nn") or str.startswith("nm") or str.startswith("nb") or str.startswith("nh") or str=="j" or str=="nis" or str=="gi"):
        return 1
    elif(str.startswith("nt") or str.startswith("nz") or str=="l" or str=="n"):
        return 2
    elif(str.startswith("x") or str.startswith("m")):
        return 3
    else:
        return 0
def not_have(string):
    if(allMentionTag.get(string) is None):
        return 1
    for title in allMentionTag[string]:
        L=-1
        for i in range(len(title)):
            if(title[i]=="（"):
                L=i+1
            elif (title[i] == "）"):
                res=title[L:i]
                if (res == "汉语词汇" or res == "词语解释" or res == "汉语词语" or res == "名称解释" or res == "名词"):
                    return 0
    return 1
def in_(res):
    if(allMentionTag.get(res)):
        if(len(allMentionTag[res])>0):
            return 1
    return 0
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
    if(ok==3):
        if(in_(ans[pos]) and jud!=3):
            if (pos - 2 >= 0 and (ans[pos + 1] == "n" or ans[pos + 1] == "nz") and (ans[pos - 1] == "x" or ans[pos - 1] == "m") and in_(ans[pos - 2] + ans[pos])):
                if(ans[pos-2] in enti):
                    enti.remove(ans[pos-2])
                enti.add(ans[pos - 2] + ans[pos])
            elif(ans[pos+1].startswith("n")):
                if (len(ans[pos]) > 1 and (ans[pos + 1] != "n" or (ans[pos + 1] == "n" and not_have(ans[pos])))):
                    enti.add(ans[pos])
    elif(ok==1) :
        if(jud==1):
            YES=1
            if (len(ans[pos])>1):
                enti.add(ans[pos])
        elif(jud==2):
            if(pos-2>=0 and (ans[pos+1]=="n" or ans[pos+1]=="nz") and (ans[pos-1]=="x" or ans[pos-1].startswith("m") or ans[pos-1]=="ntc") and in_(ans[pos-2]+ans[pos])):
                if (ans[pos - 2] in enti):
                    enti.remove(ans[pos - 2])
                enti.add(ans[pos-2]+ans[pos])
                YES=1
            elif (pos - 2 >= 0 and (ans[pos + 1] == "n") and (ans[pos - 1] == "nz") and in_(ans[pos - 2] + ans[pos])):
                if (ans[pos - 2] in enti):
                    enti.remove(ans[pos - 2])
                enti.add(ans[pos - 2] + ans[pos])
                YES = 1
            elif(in_(ans[pos])):
                if (len(ans[pos])>1 and (ans[pos+1]!="n" or (ans[pos+1]=="n" and not_have(ans[pos])))):
                    enti.add(ans[pos])
                    YES = 1
        elif(jud==3):
            if ((pos - 2 >= 0 and (ans[pos - 1] == "n" or ans[pos - 1] == "nz" or ans[pos-1]== "nrf" or ans[pos-1]== "ntc")) and in_(ans[pos-2]+ans[pos])):
                if(ans[pos-2] in enti):
                    enti.remove(ans[pos-2])
                enti.add(ans[pos-2]+ans[pos])
                YES = 1
            elif (ans[pos+1]=="x" and len(ans[pos])>2):
                if(in_(ans[pos])):
                    enti.add(ans[pos])
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
        else:
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

def div_to_excle4(ans,A,B,C):  #     ans-细粒度，A-正确答案，B-baseline，C-test。
    f = open(ans, "r",encoding="utf-8")
    f2 = open(A, "r")
    f3 = open(B, "r")
    f4 = open(C, "r")
    out=open("划分结果.txt","w")
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
def div_to_excle3(ans,A,B):  #     ans-细粒度，A-正确答案，B-test。
    f = open(ans, "r",encoding="utf-8")
    f2 = open(A, "r")
    f3 = open(B, "r")
    out=open("划分结果.txt","w")
    for line2 in f2:
        line=f.readline()
        line=f.readline()
        line3=f3.readline()
        line=line[0:len(line)-1]
        if(len(line2.split())) :
            line2 = line2.split()[0]
        else :
            line2 = ""
        line3 = line3[0:len(line3) - 1]
        out.write(line+"\t\t"+line2+"\t"+line3+"\n")
    out.close()
    f3.close()
    f2.close()
    f.close()

if __name__ == '__main__':
    allMentionTag.clear()
    fr = open('allMention.pkl', 'rb')
    allMentionTag = pickle.load(fr)
    fr.close()
    do_date("分词结果.txt")
    get_ans("第二列2.txt", "标准输出.txt")
    get_ans("第二列.txt", "标准输出.txt")
    #div_to_excle4("分词结果.txt", "标准输出.txt", "第二列.txt", "第二列2.txt")
    div_to_excle3("分词结果.txt", "标准输出.txt", "第二列2.txt")