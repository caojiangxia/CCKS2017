# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 10:14:11 2017

@author: ethel
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 10:56:01 2017

@author: ethel
"""

import sys
import urllib2
from lxml import etree
reload(sys)
sys.setdefaultencoding('utf8')
def _processAPI():
#    k = open('1.txt','wb')
    url = 'http://kw.fudan.edu.cn/cndbpedia/search/?mention=复旦大学&entity=复旦大学'
    print type(url)    
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    html = response.read().decode('utf-8')
    tree=etree.HTML(html)
#    k.write(html.encode('utf-8'))
#锚文本    
    url_list = tree.xpath('//div[@class="panel panel-default"]//a[@href]')
    url_list = [ "".join(anchor.xpath('@href')) for anchor in url_list  if "".join(anchor.xpath('@href')).startswith('./?mention')]
    print len(url_list)
    for anchor in url_list:
        print anchor

#摘要
    infomation_text = "".join(tree.xpath('//div[@id="collapseInformation"]/div/div[@class="well"]')[0].xpath('string(.)'))
    print "infomation_text:",infomation_text
    
#infobox
    name_list = tree.xpath('//div[@id="collapseInfoBox"]//td[@class="col-xs-4"]/text()')
    value_list = tree.xpath('//div[@id="collapseInfoBox"]//td[@class="col-xs-6"]') 
    info_dict = ["==>".join([elem_name.strip(),elem_value.xpath('string(.)').strip()]) \
    for elem_name,elem_value in zip(name_list, value_list)]
    print len(info_dict)
    for item in info_dict:
        print  item.split('==>')[0],item.split('==>')[1]
#tag
    tag_list = tree.xpath('//div[@id="collapseCategory"]//td[@class="col-xs-6"]')     
    for item in tag_list:
        if item.xpath('string(.)').strip()!='标签':
            print item.xpath('string(.)').strip()
#type
    tag_list = tree.xpath('//div[@id="collapseClass2"]//td[@class="col-xs-6"]')     
    for item in tag_list:
        if item.xpath('string(.)').strip()!='rdf:type':
            print item.xpath('string(.)').strip()
#primary   
    url_primary = 'http://knowledgeworks.cn:30001/?inpage=1&p=南京'
    request = urllib2.Request(url_primary)
    response = urllib2.urlopen(request)
    html = response.read().decode('utf-8')
    tree=etree.HTML(html)
    primary_title = tree.xpath('//div[@class="row"]/h3/text()')
    for title in primary_title[1:]:
        if title.strip().endswith('*primary'):
            print "%s 's primary value is 1, others are zero"%title.split('\t')[0].strip()
            break
# title 排名
    url_primary = 'http://baike.baidu.com/item/上海'
    request = urllib2.Request(url_primary)
    response = urllib2.urlopen(request)
    html = response.read().decode('utf-8')
    tree=etree.HTML(html)
    if not tree.xpath('//div[@class="lemma-summary"]'):
        poly_list = tree.xpath('//ul[@class="custom_dot  para-list list-paddingleft-1"]/li/div')
    else:
        poly_list = tree.xpath('//li[@class="item"]')
    for poly in poly_list:
        print poly.xpath('string(.)').strip()


if __name__ == '__main__':
    _processAPI()

    
    
    