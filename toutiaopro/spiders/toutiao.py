import scrapy
from selenium import webdriver
from toutiaopro.items import ToutiaoproItem
from time import sleep
from scrapy.http import HtmlResponse

class ToutiaoSpider(scrapy.Spider):
    name = 'toutiao'
    data = input("请输入要爬取的关键字:")
    number = int(input("请输入要爬取的数量:"))  # 控制爬取数量
    address = 'https://www.toutiao.com/search/?keyword='+data
    start_urls = [address]
    urls = []
    num = 0 #控制浏览器下滑循环次数
    index = 0 #控制收集连接条数


    #初始化浏览器
    def __init__(self):
        #根据自己的chrome驱动路径设置
        path = r'H:\PythonCode\Spider\scrapy\wangyi\wangyi\spiders\chromedriver.exe'
        self.bro1 = webdriver.Chrome(executable_path=path)
        self.bro2 = webdriver.Chrome(executable_path=path)


    #获取到关键字的文章列表
    def parse(self, response):
        #获取到列表属性
        div_list = response.xpath('/html/body/div/div[4]/div[2]/div[3]/div/div/div')

        ########
        #获取每篇文章
        # for div in div_list:
        #     url_temp = div.xpath('./div/div/div/div/div//@href').extract_first()
        #     url = 'https://www.toutiao.com/a'+url_temp.split('/',3)[2]
        #     self.urls.append(url)
        # for href in self.urls:
        #     yield scrapy.Request(href,callback=self.parse_model)
        ##############

        for div in div_list:
            url_temp = div.xpath('./div/div/div/div/div//@href').extract_first()
            #链接拼接
            url = 'https://www.toutiao.com/a'+url_temp.split('/',3)[2]
            self.urls.append(url)
            print("--------")
            print(url)
            print("---------")

        #控制爬取数量
        while self.index<=self.number:
            # for href in self.urls:
            #     yield scrapy.Request(href, callback=self.parse_model)
            index = self.index
            yield scrapy.Request(self.urls[index], callback=self.parse_model)

            #获取10篇文章后刷新文章列表
            #有些关键字一页若没有这个数，则需调低阈值
            if self.num == 5:
                #滑动滚动条
                self.bro1.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                sleep(5)
                page_text = self.bro1.page_source
                print("if里面")
                #print(page_text)

                new_response = HtmlResponse(url='',body=page_text,encoding='utf-8', request='')
                # self.artical_list(page_text)
                self.artical_list(new_response)
                self.num = 0
                self.index = self.index + 1
                print("if中的index", self.index)
            else:
                print("else里面",self.num)
                self.index = self.index + 1
                print("else中的index",self.index)
                self.num = self.num + 1
    #文章解析
    def parse_model(self,response):

        title = response.xpath('//*[@id="root"]/div/div[2]/div[1]/div[2]/h1/text()').extract_first()
        content = response.xpath('//*[@id="root"]/div/div[2]/div[1]/div[2]/article//text()').extract()
        content = ''.join(content)
        span = response.xpath('//*[@id="root"]/div/div[2]/div[1]/div[2]/div[1]/span')
        if len(span) == 2:
            author = response.xpath('//*[@id="root"]/div/div[2]/div[1]/div[2]/div[1]/span[1]/text()').extract_first()
            time = response.xpath('//*[@id="root"]/div/div[2]/div[1]/div[2]/div[1]/span[2]/text()').extract_first()
        else:
            author = response.xpath('//*[@id="root"]/div/div[2]/div[1]/div[2]/div[1]/span[2]/text()').extract_first()
            time = response.xpath('//*[@id="root"]/div/div[2]/div[1]/div[2]/div[1]/span[3]/text()').extract_first()

        #提交管道
        #self.bro1.excute_script('window.scrollTo(0, document.body.scrollHeight)')
        item = ToutiaoproItem()
        item['title'] = title
        item['content'] = content
        item['time'] = time
        item['author'] = author

        yield item

    #列表解析
    def artical_list(self,new_response):
        # 获取到列表属性
        div_list = new_response.xpath('/html/body/div/div[4]/div[2]/div[3]/div/div/div')
        num_urls = len(self.urls)
        num_div = len(div_list)
        for div in range(num_urls,num_div):
            href_temp = div_list[div].xpath('./div/div/div/div/div//@href').extract_first()
            href_temp = 'https://www.toutiao.com/a'+href_temp.split('/',3)[2]
            self.urls.append(href_temp)
            print("!!!!!!!!!!!!!")
            print(href_temp)
            print("!!!!!!!!!!!!")