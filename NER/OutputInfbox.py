import threadpool
import urllib.request
import urllib.response
from urllib.parse import quote
import re
import pickle
allMention={}
out=open("MentionTitleInf.txt","w",encoding="utf-8")
def Outoput(mention,title,abstract):
    out.write(mention+"\n"+title+"\n"+abstract+"\n")
if __name__ == '__main__':
    allMention.clear()
    fr = open('allMention.pkl', 'rb')
    allMention = pickle.load(fr)
    fr.close()
    for mention in allMention:
        for title in allMention[mention]:
            if(title.strip()=="primary"):
                continue
            if(allMention[mention][title].get("abstract") is not None):
                if(allMention[mention][title]["abstract"]=="") :
                    continue
                Outoput(mention.strip(),title.strip(),allMention[mention][title]["abstract"].strip())
    out.close()