#coding=utf-8
import threadpool
import urllib.request
import urllib.response
from urllib.parse import quote
import socket
import pickle

'''暂时不用
*************************************************************************************************
def find_ans(str):
    res = urllib.request.urlopen("http://knowledgeworks.cn:30001/?p="+quote(str))
    return  (res.read().decode("utf-8"))

def get_url(str):
    return "http://knowledgeworks.cn:30001/?p="+quote(str)

def file_view(name):
    f = open(name, 'r', encoding='utf-8')  # 打开ans文件需要这样做
    for line in f:
        print(line)

'''

'''
 #这一部分代码是用来处理SWJTU处理后的划分词并去爬去title,注意几个地方
1.这里有两个api
2.打开文件为ans.txt
3.输出的文件为gbk编码
http://knowledgeworks.cn:20313/cndbpedia/api/entity?mention=   {"entity": []}
http://knowledgeworks.cn:30001/?p=     ["Unknown Mention"]
*************************************************************************************************
'''
timeout = 10
socket.setdefaulttimeout(timeout)
allMentionentity={}
se=set()
se_c=set()
out=open('crawlAPI1.txt', 'w')#在爬百科时用到
out2=open('crawlAPI2.txt', 'w')#在爬百科时用到
out3=open("CannotCrawl.txt","w")
count=0
ok=0
def load_date(name):
    global se
    f = open(name, 'r', encoding='utf-8')
    data=[]
    dat=[]
    for line in f:
        dat.clear()
        for res in line.split():
            RES=""
            for i in range(len(res)):
                if(res[i]=='['):
                    continue
                if(res[i]=='/'):
                    if(RES not in se):
                        se.add(RES)
                    dat.append(RES)
                    break
                RES+=res[i]
        leng=len(dat)
        end=leng
        while(leng>0):
            beg = 0
            while(beg+leng<=end):
                RES=""
                for i in range(beg,beg+leng):
                    RES+=dat[i]
                if (RES not in se):
                    se.add(RES)
                beg+=1
            leng-=1
    f.close()
    for i in se:
        data.append(i)
    return data
def find_ans2(str):
    global out,out3,out2
    global count
    count += 1
    if (count % 100 == 0):  # 查看进度
        print(count)
    res = urllib.request.urlopen("http://knowledgeworks.cn:20313/cndbpedia/api/entity?mention=" + quote(str))
    try:
        ans = res.read().decode("utf-8")
        if (str + "##" in se_c):
            return
        se_c.add(str + "##")
        try:
            out2.write(str + " " + ans + "\n")
        except:
            if(ok==0):
                out3.write(str + "\n")
    except:
        ans = res.read().decode("gbk")
        if (str + "##" in se_c):
            return
        se_c.add(str + "##")
        try:
            out2.write(str + " " + ans + "\n")
        except:
            if (ok == 0):
                out3.write(str + "\n")
def find_ans(str):
    global out, out3, out2
    global count
    count+=1
    if(count%100==0):#查看进度
        print(count)
    res = urllib.request.urlopen("http://knowledgeworks.cn:30001/?p="+quote(str))
    try:
        ans=res.read().decode("utf-8")
        if(str+"#" in se_c):
            return
        se_c.add(str+"#")
        try:
            out.write(str + " " + ans + "\n")
        except:
            if (ok == 0):
                out3.write(str+"\n")
    except :
        ans = res.read().decode("gbk")
        if (str + "#" in se_c):
            return
        se_c.add(str + "#")
        try:
            out.write(str + " " + ans + "\n")
        except:
            if (ok == 0):
                out3.write(str+"\n")
def get_output(data):
    pool = threadpool.ThreadPool(40)
    requests = threadpool.makeRequests(find_ans, data)
    [pool.putRequest(req) for req in requests]
    pool.wait()
def get_output2(data):
    pool = threadpool.ThreadPool(40)
    requests = threadpool.makeRequests(find_ans2, data)
    [pool.putRequest(req) for req in requests]
    pool.wait()
def fill(name):
    f=open(name,"r")
    data=[]
    for line in f:
        data.append(line)
    f.close()
    out=open("do_crawlAPI1","w")
    for line in data:
        try:
            line.index("Unknown Mention")
        except :
            out.write(line)
    out.close()
def fill2(name):
    f=open(name,"r")
    data=[]
    for line in f:
        data.append(line)
    f.close()
    out=open("do_crawlAPI2","w")
    for line in data:
        try:
            line.index("[]")
        except :
            out.write(line)
    out.close()
def open_miss(name):
    miss=open(name,"r")
    data=[]
    for line in miss:
        line.strip()
        data.append(line)
    miss.close()
    return data
if __name__ == '__main__':
    data=load_date("分词结果.txt")
    print(len(se))
    get_output(data)
    get_output2(data)
    out3.close()
    out2.close()
    out.close()
    ok=1
    # for i in range(1,10):
    #     data=open_miss("CannotCrawl.txt")
    #     get_output(data)
    #     get_output2(data)
    print(len(se_c))
    print(len(se))
    fill("crawlAPI1.txt")
    fill2("crawlAPI2.txt")