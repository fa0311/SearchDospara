import requests
from dataclasses import dataclass
import datetime
import re
import xml.etree.ElementTree as et



class SearchDospara:
    def __init__(self):
        self.url = "https://www.dospara.co.jp/5shopping/search.php"
        self.params = {
            "ft": "",
            "gosearch": "検索"
        }
        self.headers = {
            "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            "Cache-Control": 'no-cache',
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        }
        self.proxies = {}
        self.pattern = '<div class="detailBtn">{line}<a href="/5shopping/detail_parts.php\?bg={number}&br={number}&sbr={number}&mkr={number}&ic={get}&ft={text}" onClick="{text}"><img src="https://www.dospara.co.jp/5shopping/templates/search/img/detail_button.png" alt="{text}"></a>{line}</div>'.format(line="[\s\S]+?",text=".+?",number="[0-9]+?",get="([0-9]+?)")

    def get(self,query):
        self.params["ft"] = query
        self.html = requests.get(url=self.url, headers=self.headers, params=self.params, proxies=self.proxies).text
        self.ids = re.findall(self.pattern, self.html)
        return [_SearchDosparaGetGpio(id,self.headers,self.proxies) for id in self.ids]
    
class _SearchDosparaGetGpio:
    def __init__(self,id,headers,proxies):
        self.url = "https://www.dospara.co.jp/5print/gpio.php"
        self.params = {
            "type": "itemdata",
            "ofm": "xml",
            "ic": id
        }
        self.headers = headers
        self.proxies = proxies
        self.namespace = {'tw': '/5print/xsd/tw-item-data.xsd'}

    def get(self):
        xml = requests.get(url=self.url, headers=self.headers, params=self.params, proxies=self.proxies).text
        doc = et.fromstring(xml)
        content = {re.findall('\{.+?\}(.+?)$', itemNode.tag)[0] : self._is_float(itemNode.text) for itemNode in doc.find('tw:saleData/tw:item',self.namespace)}
        return _SearchDosparaContent(**content)

    def _is_float(self,s):
        try:
            return int(s) if int(s) == int(float(s)) else float(s)
        except:
            return s
        
@dataclass
class _SearchDosparaContent:
    itemcode:int  = None
    brgroupcode:int  = None
    brcode:int  = None
    sbrcode:int  = None
    brname:str  = None
    sbrname:str  = None
    itemname:str  = None
    uriamt_tax:int  = None
    uriamt_notax:int  = None
    asmseturiamt_tax:int  = None
    asmseturiamt_notax:int  = None
    spamt_tax:int  = None
    spamt_notax:int  = None
    spdjflg:int  = None
    mkrname:str  = None
    mkrcode:int  = None
    soldout_flg:int  = None
    itemimg_url:str  = None
    stkname:str  = None
    simplespec:str  = None
    urisdate:str  = None
    pointrate:float   = None
    pointback:int   = None
    rakutenrate:float   = None
    rakutenback:float   = None
    camppointrate:float   = None
    camppoint:int   = None
    ratsum:float   = None
    pointcaslesssum:int  = None
