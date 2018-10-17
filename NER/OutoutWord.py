import threadpool
import urllib.request
import urllib.response
from urllib.parse import quote
import re
import pickle

if __name__ == '__main__':
    f=open("划分结果.txt","r")
    out = {}
    allword=set()
    for line in f:
        line=line.strip()
        line=line.split("\t")
        if (len(line)>=3):
            res=line[2]
            res=res.split("|||")
            for word in res:
                allword.add(word)
                if (out.get(word) is None):
                    out[word] = 0
                out[word] -= 1
    f.close()
    # f = open("划分结果.txt", "r")
    # for line in f:
    #     line = line.strip()
    #     line = line.split("\t")
    #     if (len(line) >= 4):
    #         res = line[3]
    #         res = res.split("|||")
    #         for word in res:
    #             if(out.get(word) is None):
    #                 out[word]=0
    #             out[word]+=1
    # out = sorted(out.items(), key=lambda d: d[1], reverse=True)
    # f.close()
    # print(out)
    f=open("word.txt","w")
    for word in allword:
        #f.write(word+"\t"+"entity"+"\n")
        f.write(word+"\n")
    f.close()