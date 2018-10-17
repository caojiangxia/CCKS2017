# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
    
class EntiyItem():
    def __init__(self):     
        self._res={}
        
    def __setitem__(self,key,val):
        self._res[key]=val
        
    def __getitem__(self,key):
        if self._res.get(key) is not None:
            return self._res[key]
    # define the fields for your item here like:
    # name = scrapy.Field()
    baike_title = ''
    baike_url = ''
    baike_info = ''
    baike_desc = ''
    baike_context = ''
    baike_nikname = []
    baike_anchor = []
