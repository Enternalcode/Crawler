# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import requests
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from qcwy.settings import logger


# 获取随机代理
class RandomProxyMiddleware():
    def __init__(self, proxypool):
        self.logger = logger
        self.proxypool = proxypool

    # 抓取代理池页面，获取ip代理（阿里云主机，port：5555）
    def get_random_proxy(self):
        try:
            response = requests.get(self.proxypool)
            if response.status_code == 200:
                proxy = response.text
                return proxy
        except requests.ConnectionError:
            return False

    # 如果request.meta['retry_times']不为空，说明请求出现错误，随即更换ip
    def process_request(self, request, spider):
        if request.meta.get('retry_times'):
            proxy = self.get_random_proxy()
            if proxy:
                uri = 'http://{proxy}'.format(proxy=proxy)
                logger.debug('正在使用代理： ' + str(uri))
                request.meta['proxy'] = uri

    @classmethod
    def from_crawler(cls, crawler):
        setting = crawler.settings
        return cls(
            proxypool=setting.get('PROXYPOOL')
        )


# 随机User-Agent
class RandomUserAgentMiddleware(UserAgentMiddleware):

    def __int__(self, user_agent):
        super().__init__(user_agent)    # 单继承super（）调用父类__init__方法
        self.user_agent = user_agent

    def process_request(self, request, spider):
        agent = random.choice(self.user_agent)
        logger.debug('正在使用User-Agent： ' + agent)
        request.headers['User-Agent'] = agent

    @classmethod
    def from_crawler(cls, crawler):
        setting = crawler.settings
        return cls(
            user_agent=setting.get('USER_AGENT_POOL')
        )