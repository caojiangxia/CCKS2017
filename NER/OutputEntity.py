import threadpool
import urllib.request
import urllib.response
from urllib.parse import quote
import re
import pickle
allMention={}
out=open("PrimaryInf.txt","w",encoding="utf-8")
def Outoput(xifenci,stan,primary,answer):
    out.write(xifenci+"*********\t"+stan+"\t"+primary+"*********\t"+answer+"\n")
def pri(word):
    if(allMention.get(word) is None):
        return "nil"
    if(allMention[word].get("primary") is None):
        return "nil"
    return allMention[word]["primary"]
def find_primary(entity):
    entity=entity.split("|||")
    ret=[]
    for word in entity:
        ret.append(pri(word))
    return "|||".join(ret)
if __name__ == '__main__':
    fr = open('allMention.pkl', 'rb')
    allMention = pickle.load(fr)
    fr.close()
    f1=open("分词结果.txt","r",encoding="utf-8")
    f2=open("标准输出.txt","r")
    f3=open("第三列2.txt","r")
    ok=0
    for xifenci in f1:
        if ok==0 :
            ok=1
            continue
        ok=0
        stan=f2.readline()
        answer=f3.readline()
        stan=stan.strip()
        answer=answer.strip()
        xifenci = xifenci.strip()
        primary=find_primary(stan.split("\t")[0])
        Outoput(xifenci,stan,primary,answer)
    f3.close()
    f2.close()
    f1.close()
    out.close()