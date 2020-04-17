from requests import get, post
from time import time, localtime, sleep
from random import randint as rnd
from re import search
class WJX():
    def __init__(self, id, answer):
        self.test_url = f'https://www.wjx.cn/jq/{id}.aspx'
        self.answer = {'hlv': 1, 'submitdata': answer}
        self.head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
        self.id = id
        self.start_time = self.get_start_time()
    def get_start_time(self):
        # return search(r'var starttime="(.*)";', self.source).groups()[0]
        t = time()
        y,m,d,h,min,s = localtime(t)[0:6]
        return f'{y}%2F{m}%2F{d}%20{h}%3A{min}%3A{s}'# 2020/4/17 12:33:50   2020%2F4%2F17%2012%3A37%3A50
    def get_rn(self): # IMPROVEMENTS NEEDED
        # return search(r'var rndnum="([0-9]*)";', self.source).groups()[0]
        return input('var rndnum="???":')
    def get_jqnonce(self):# IMPROVEMENTS NEEDED
        # return search(r'var jqnonce="(.*)";', self.source).groups()[0]
        return input('var jqnonce="???":')
    def get_jqsign(self, ktimes, jqnonce):# a = jqnonce
        '''https://image.wjx.com/joinnew/js/jqnew2.js?v=1186
                function dataenc(a) {
            var c, d, e, b = ktimes % 10;
            for (0 == b && (b = 1),
            c = [],
            d = 0; d < a.length; d++)
                e = a.charCodeAt(d) ^ b,
                c.push(String.fromCharCode(e));
            return c.join("")
        }
        ''' 
        b = ktimes % 10
        if 0 == b:
            b = 1
        c = []
        for d in range(len(jqnonce)):
            e = ord(jqnonce[d]) ^ b
            c.append(chr(e))
        return ''.join(c)
    def send(self):
        r = get(self.test_url, headers=self.head)
        self.cookie = r.cookies
        self.source = r.text
        t = int(time())*1000 + rnd(100, 200)
        ktimes = rnd(16,40)
        sleep(rnd(2,4))
        jqnonce = self.get_jqnonce()
        '''数据说明
            'hlv':1,
            'curID':self.id, # 问卷id
            't':, # 提交数据时间戳
            'starttime':, # 打开网页时间  "2020/4/16 17:05:07";
            'ktimes':, # 答题时间（不是秒数）
            'rn':, # 可获取  var rndnum="xxxxxx";
            'jqnonce':, # 可获取  e.g. r'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxx'
            'jqsign':, # 加密验证  e.g. r'%3Eb04%3Fb1d*1631*3d%3Ed*%3F551*53f13fde65f%3E'
        '''
        # self.head['X-Forwarded-For'] = f'{rnd(64, 68)}.{rnd(0,255)}.{rnd(0,255)}.{rnd(0,255)}'
        post_url = f'https://www.wjx.cn/joinnew/processjq.ashx?submittype=1&curID={self.id}&t={t}&starttime={self.start_time}&ktimes={ktimes}&rn={self.get_rn()}&jqnonce={jqnonce}&jqsign={self.get_jqsign(ktimes, jqnonce)}'
        r = post(post_url, headers=self.head, data=self.answer, cookies=self.cookie)
        return r
test = WJX('问卷id','你的答案（例：1$2}2$1 意为第一套选B，第二题选A）')
print(test.send().text)
