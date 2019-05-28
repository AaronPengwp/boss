# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html


import random
import requests
import json
from boss.models import ProxyModel
from twisted.internet.defer import DeferredLock


# 随机请求头
class UserAgentDownloadMiddleware(object):
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Browzar)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; MyIE2; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0)'
    ]

    def process_request(self, request, spider):
        user_agent = random.choice(self.USER_AGENTS)
        request.headers['User-Agent'] = user_agent



class IPProxyDownloadMiddleware(object):
    PROXY_URL = 'http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=&city=0&yys=0&port=11&time=1&ts=1&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions='



    def __init__(self):
        super(IPProxyDownloadMiddleware, self).__init__()
        self.current_proxy = None
        self.lock = DeferredLock()



    def process_request(self, request, spider):
        if 'proxy' not in request.meta or self.current_proxy.is_expiring:
            # 请求代理
            self.update_proxy()

    def process_response(self, request, response, spider):
        if response.status != 200 or "captcha" in response.url: #有captcha 说明跳到验证码页面了
            if not self.current_proxy.blacked:
                self.current_proxy.blacked = True
            print('%s这个代理被拉入黑名单了'%self.current_proxy.ip)
            self.upate_proxy()
            # 如果到这里，说明这个请求已经被boss直聘识别为爬虫了
            # 所以这个请求就相当于什么都没有获取到
            # 如果不返回request,那么这个request就相当于没有获取到数据
            # 也就是说，这个请求就被废掉了，这个数据就没有被抓取到
            # 所以要重新返回request,让这个请求重新加入到调度中。
            # 下次再发送
            return request
        # 如果是正常的，那么要记得返回response
        # 如果不返回，那么这个resposne就不会被传到爬虫那里去
        # 也就得不到解析
        return response

    def update_proxy(self):
        self.lock.acquire()  # 因为scrapy是异步的，所以要加锁
        if not self.current_proxy or self.current_proxy.is_expiring or self.current_proxy.blacked:
            response = requests.get(self.PROXY_URL)
            text = response.text
            print('重新获取一个代理:', text)
            result = json.loads(text)
            if len(result['data']) > 0:  #防止频繁的获取芝麻代理，不然返回空信息
                data = result['data'][0]
                proxy_model = ProxyModel(data) #实例化的时候会把blacked设置成False
                self.current_proxy = proxy_model

        self.lock.release()
