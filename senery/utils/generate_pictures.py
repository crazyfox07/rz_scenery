# -*- coding:utf-8 -*-
"""
File Name: generate_pictures
Version:
Description:
Author: liuxuewen
Date: 2017/8/7 13:56
"""
import asyncio
import aiohttp
import time
from bs4 import BeautifulSoup
import re
from senery.utils.proxies import get_aws_proxies
import os
import hashlib
import json
from asyncio import Semaphore

import datetime

sema=Semaphore(3)

class RZ_Senery(object):

    def __init__(self):
        self.start_url='https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1502087034921_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&hs=2&word=%E6%97%A5%E7%85%A7%E6%B5%B7%E6%99%AF%E5%A3%81%E7%BA%B8'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',

            'Upgrade-Insecure-Requests':'1',
            }

    async def save_image(self,img):
        path=os.path.dirname(os.path.dirname(__file__))+'/static/imgs'
        if not os.path.exists(path):
            os.makedirs(path)
        num=len(os.listdir(path))
        m=hashlib.md5()
        m.update(str(time.time()).encode('utf-8'))
        pic_name='{}_{}.jpg'.format(m.hexdigest(),num)
        with open('{}/{}'.format(path,pic_name),'wb') as f:
            content=await self.get_content(img)
            f.write(content)

    async def get_content(self,url):
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url, proxy=get_aws_proxies()['http']) as res:
                text = await res.read()
                return text

    async def get_html(self,url):
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url, proxy=get_aws_proxies()['http']) as res:
                text = await res.text()
                return text
    async def get_json(self,url):
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url, proxy=get_aws_proxies()['http']) as res:
                text = await res.json()
                return text

    async def crawl(self,page):
        url=self.start_url
        html=await self.get_html(url)
        imgs=re.findall(r'"objURL":"(.*?)"',html,re.S)
        print(imgs)
        [await self.save_image(img) for img in imgs]

    async def crawl_json(self,page):
        with (await sema):
            url='https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E6%97%A5%E7%85%A7%E6%B5%B7%E6%99%AF%E5%A3%81%E7%BA%B8&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E6%97%A5%E7%85%A7%E6%B5%B7%E6%99%AF%E5%A3%81%E7%BA%B8&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn={}&rn=30'.format(page*30)
            result=await self.get_html(url)
            result=json.loads(result)
            imgs=[item['middleURL'] for item in result['data'][:-1]]
            [await self.save_image(img) for img in imgs]



def crawl():
    begin = time.time()
    rz_scenery = RZ_Senery()
    loop = asyncio.get_event_loop()
    tasks = [rz_scenery.crawl_json(page) for page in range(10,100)]
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
    end = time.time()
    print(end - begin)


def save_to_mongodb():
    from pymongo import MongoClient
    conn = MongoClient('127.0.0.1', 27017)
    my_db = conn.mydb
    my_set = my_db.rz_scenery
    for picture in os.listdir('D:/project/rz/rz_scenery/senery/static/imgs'):
        photo_name = picture
        photo_url = 'D:/project/rz/rz_scenery/senery/static/imgs/{}'.format(photo_name)
        pub_date = datetime.datetime.now()
        my_set.insert({'photo_name':photo_name,'photo_url':photo_url,'pub_date':pub_date})


if __name__ == '__main__':
    #crawl()
    # path=os.path.join(os.path.dirname(os.path.dirname(__file__)),'static/imgs')
    # print(path)
    print('begin:')
    begin=time.time()
    save_to_mongodb()
    end=time.time()
    print('time use: {}'.format(end-begin))



