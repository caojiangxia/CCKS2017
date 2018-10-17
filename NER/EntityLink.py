# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 19:08:19 2017

@author: ethel
"""
#graph-based candidates ranking
#entropy-based NIL prediction
#摘要+窗口50的上下文
import sys
import os
import json
import math
import pickle
import numpy as np
from numpy import dot,eye
from numpy.linalg import inv
from items import EntiyItem
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity


stpwrdpath = 'stopwords.dat'

#从文件导入停用词表
stpwrd_dic = open(stpwrdpath, 'rb')
stpwrd_content = stpwrd_dic.read()
stpwrdlst = stpwrd_content.splitlines()
stpwrd_dic.close()
    
def entLinkRead(mentionLst):
    mention2context = []
    mention2candidates = {}
    menlst = mentionLst[0]
    menContext = mentionLst[1]
    for men, titleLst in zip(menlst,mentionLst[2]):
        mencon_tuple = (men, menContext)
        mention2context.append(mencon_tuple)
        candidates_list = []
        for title in titleLst:
            item = EntiyItem()
            item['baike_title'] = title
            item['baike_context'] = mentionLst[3][title]
            item['baike_anchor'] =  mentionLst[4][title]
            candidates_list.append(item)
        mention2candidates[men] = candidates_list
    mention_tf =_get_mention_weight(mention2context)
    mention2entiy = _rank_candidate(mention2candidates, mention_tf, mention2context)
    RET=[]
    ANS = ""
    for men, titleLst, scores in zip(menlst,mentionLst[2],mention2entiy):
        candidates_list = mention2candidates[men]
        if not candidates_list:
            RET.append("nil")
            continue
            #print(men,"has no candidates!")
        else:
            MAX=-1
            ANS=""
            for i in range(len(candidates_list)):
                if(float(scores[0,i])>MAX+0.000000001):
                    MAX=float(scores[0,i])
                    ANS=candidates_list[i]['baike_title']
                #print(candidates_list[i]['baike_title'],  scores[0,i])
            RET.append(ANS)
    # for men, titleLst, scores in zip(menlst,mentionLst[2],mention2entiy):
    #     candidates_list = mention2candidates[men]
    #     if not candidates_list:
    #         print(men,"has no candidates!")
    #     else:
    #         for i in range(len(candidates_list)):
    #             print(candidates_list[i]['baike_title'],  scores[0,i])
    return RET
#------------------------------------------------------------------------------   
def _get_mention_weight(mention2context):
    #Entity liking
    mention_tf = dict()
    imen = len(mention2context)
    for mention,_ in mention2context:
        if mention_tf.get(mention) is None:
            mention_tf[mention] = 1.0/imen
        else:
            mention_tf[mention] +=1.0/imen
    return mention_tf
#---------------------------------------------------------------------        
def _rank_candidate(mention2candidates,mention_tf,mention2context):
#    print 'Start to rank candidates!'    
    #输出新闻语料中所有mention的对应实体
    imen = len(mention2context)
    mention2entiy = []
    idxnode = []
    idxmention = []
    idx = -1
    parent = {}
    mention2csim = []
    for tu in mention2context:
        mention = tu[0]
        context = tu[1]
        corpus = ["\t".join(context)]
        candidates_list = mention2candidates[mention]
        ilen = len(candidates_list)
        idxnode.append(tu)
        idx +=1
        idxmention.append(idx)
        ifather = idx
        if not candidates_list:
            mention2csim.append(None)
        else:
            for it in candidates_list:
                corpus.append(it['baike_context'])
                idxnode.append(it)
                idx +=1
                parent[idx] = ifather
            # print "corpus:",json.dumps(corpus, encoding="UTF-8", ensure_ascii=False)
            sims = compareContext(corpus,stpwrdlst)
            mention2csim.append(sims)          
#--------------------------------------------------------------------- 
    #计算propagation matrix
    inum = len(idxnode)
    dImportance = np.zeros([inum,1],dtype=np.float)
    Matrix_Propagation = np.zeros([inum,inum],dtype=np.float)
    idx = 0
    for i in range(inum):
        if isinstance(idxnode[i],EntiyItem):
            ifather = parent[i]
            mention = idxnode[ifather][0]
            candidates_list = mention2candidates[mention]
            ilen = len(candidates_list)
            neighbor_list = [j for j in list(range(0,ifather))+list(range(ifather+1+ilen,inum)) if isinstance(idxnode[j],EntiyItem) \
            and i!=j and idxnode[parent[i]][0] != idxnode[parent[j]][0]]
            relsims = [semanticRelate(idxnode[i]['baike_anchor'], idxnode[j]['baike_anchor']) \
            if idxnode[i]['baike_anchor'] and idxnode[j]['baike_anchor'] else 0.0 \
            for j in neighbor_list]          
            np_rels = np.asarray(relsims) 
            if np.sum(np_rels)!=0:
                prels = list(np_rels/(1.0*np.sum(np_rels)))
                for j,prel,k in zip(neighbor_list,prels,np_rels):
                    Matrix_Propagation[j,i] = prel
        else:         
            mention = idxnode[i][0]
            dImportance[i,0] = mention_tf[mention]
            candidates_list = mention2candidates[mention]
            if candidates_list:
                ilen = len(candidates_list)
                sims = mention2csim[idx][0]
                idx +=1
                if np.sum(sims)!=0:
                    psims = sims/(1.0*np.sum(sims))
                    for j in range(i+1,i+1+ilen):
                        Matrix_Propagation[j,i] = psims[j-i-1]
            else:
                idx +=1
#---------------------------------------------------------------------
    #计算evidence score vector   
    idx = 0
    I = eye(inum, dtype=np.float)
#    dImportance = dImportance/np.sum(dImportance,axis=0)
    evidence = 0.1 * dot(inv(I-0.9*Matrix_Propagation),dImportance)
    score = evidence.reshape([1,inum]) 
    for i in range(imen):
        mention = idxnode[idxmention[i]][0]
        candidates_list = mention2candidates[mention]
        if not candidates_list:
            mention2entiy.append(None)
#            logger.info("Cannot Find KB Entities for Mention %s!"%(mention))
        else:           
            ilen = len(candidates_list)
            sims = mention2csim[idx]
            dsum = np.sum(sims[0])
            maxidx = (score[:, idxmention[i] + 1:idxmention[i] + 1 + ilen])
            # print (score[:,idxmention[i]+1:idxmention[i]+1+ilen])
            # print(score[:, idxmention[i] + 1:idxmention[i] + 1 + ilen])
            # if dsum!=0:
            #     maxidx = (score[:,idxmention[i]+1:idxmention[i]+1+ilen]*sims)
            # else:
            #     maxidx = score[:,idxmention[i]+1:idxmention[i]+1+ilen]
#            logger.info("-->[DEBUG] Debug %s's target entity-----------------"%(mention))
#--------------------------------
            targetEnt = candidates_list[maxidx.argmax(axis=1)[0]]
            mention2entiy.append(maxidx)
        idx +=1           
    return mention2entiy

#-----------------------util------------------------------------
def mul(A,B):
    A=np.asarray(A)
    B = np.asarray(B)
    AA=np.sqrt(np.sum(A**2))
    BB = np.sqrt(np.sum(B ** 2))
    if(AA*BB==0):
        return int(1)
    return AA*BB
def _calculate(corpus):
    n=len(corpus)
    m=len(corpus[0])
    A=np.asarray(corpus[0])
    B=np.asarray(corpus[1:n])
    A=A.reshape(1,m)
    B=B.transpose()
    sims = np.dot(A,B)
    a=sims
    for i in range(len(a)):
        for j in range(len(a[i])):
            a[i][j]=a[i][j]/mul(corpus[i],corpus[j+1])
    sims=np.asarray(a)
    maxsim =sims.max(axis=1)[0]
    maxidx = sims.argmax(axis=1)[0]
    #print(sims)
    return sims
def getvector(allword,all):
    ret=[]
    for word in allword:
        if all.get(word) is not None:
            ret.append(float(all[word]))
        else:
            ret.append(float(0))
    return ret
def init(corpus):
    allword=set()
    all={}
    ret=[]
    for i in range(len(corpus)):
        res=corpus[i].split("\t")
        for j in range(len(res)):
            allword.add(res[j])
    for i in range(len(corpus)):
        res = corpus[i].split("\t")
        all.clear()
        for j in range(len(res)):
            if(all.get(res[j]) is None):
                all[res[j]]=0
            all[res[j]]+=1
        ret.append(getvector(allword,all))
    return ret
def compareContext(corpus,stpwrdlst):
    RES=init(corpus)
    sims = _calculate(RES)
#    maxsim = sims.max(axis=1)[0]
#    maxidx = sims.argmax(axis=1)[0]
    return sims

def semanticRelate(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    inter = len(set1 & set2)
    if inter>0:
        return 1-(math.log10(max(len(set1),len(set2)))-math.log10(inter))/(math.log10(10000000)-math.log10(min(len(set1),len(set2))))
    else:
        return 0.0

# if __name__ == '__main__':
#     fr = open('LIST.pkl', 'rb')
#     mentionLst = pickle.load(fr)
#     fr.close()
#     for item in mentionLst:
#         print(item)
#     entLinkRead(mentionLst)

 