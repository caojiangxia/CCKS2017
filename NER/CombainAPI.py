#coding=utf-8
import threadpool
import urllib.request
import urllib.response
from urllib.parse import quote
import pickle
answer={}
def file_open(name):
    f=open(name,"r")
    for line in f :
        string1=line.split()[0].strip()
        if(answer.get(string1) is None):
            answer[string1]=set()
        L=-1
        for i in range(len(line)):
            if(L==-1 and line[i]=="\""):
                L=i+1
            elif(L!=-1 and line[i]=="\""):
                if(line[L:i]!="Unknown Mention" and line[L:i]!="entity"):
                    answer[string1].add(line[L:i].strip())
                L=-1
    f.close()
if __name__ == '__main__':
    file_open("网址一爬取结果处理后.txt")
    file_open("网址二爬取结果处理后.txt")
    print(answer["oppo手机"])
    fw = open('allMentionTitle2.pkl', 'wb')
    pickle.dump(answer, fw, -1)
    fw.close()
    fr = open('answer.pkl', 'rb')
    answer = pickle.load(fr)
    fr.close()
    print(answer)