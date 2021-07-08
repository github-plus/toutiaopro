# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse
from time import sleep
import random

class ToutiaoproDownloaderMiddleware:

    #代理池
    PROXY_https = [
        '120.83.49.90:9000',
        '95.189.112.214:35508',

    ]
    def process_request(self, request, spider):

        # ip = random.choice(self.PROXY_https)
        # request.meta['proxy'] = 'https://' + ip
        return None

    def process_response(self, request, response, spider):
        bro1 = spider.bro1 #文章列表浏览器
        bro2 = spider.bro2 #具体文章浏览器
        #请求地址在文章列表里
        if request.url in spider.urls:
            bro2.get(request.url)
            sleep(2)
            page_text = bro2.page_source
            new_response = HtmlResponse(url=request.url, body=page_text, encoding='utf-8', request=request)
            return new_response
        else:
            bro1.get(request.url)
            sleep(2)
            page_text = bro1.page_source

            response = HtmlResponse(url=request.url, body=page_text, encoding='utf-8', request=request)

            return response

    def process_exception(self, request, exception, spider):
        #代理异常
        # ip = random.choice(self.PROXY_https)
        # request.meta['proxy'] = 'https://' + ip
        #
        # return request
        pass

