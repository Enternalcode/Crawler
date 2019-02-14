# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from qcwy.items import QcwyItem
from qcwy.settings import KEYWORD, logger


class QianchengSpider(Spider):
    # 关键词 页数 最大查询页数
    keyword = KEYWORD
    name = 'qc'
    # 前程无忧索引页网址
    base_urls = f'https://search.51job.com/list/000000,000000,0000,00,9,99,{keyword},2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=?'

    # 搜索页添加关键词
    def start_requests(self):
        yield Request(self.base_urls, callback=self.parse_detail_urls, dont_filter=True)

    def parse_detail_urls(self, response):
        """
        为了增量爬取，索引页皆不过滤;只对详情页去重
        """
        detail_urls = response.css('p.t1 span a::attr(href)').extract()
        for url in detail_urls:
            # 去重详情页
            yield Request(url=url, callback=self.parse_detail)
        try:
            next_page_url = response.css('.p_in li:nth-child(8) a::attr(href)').extract_first()
            if next_page_url:
                yield Request(next_page_url, callback=self.parse_detail_urls, dont_filter=True)
        except:
            logger.debug('无下页链接')

    def parse_detail(self, response):  # 解析详情页,得到目标信息
        """
        目标信息: 职位名称|薪酬水平|城市|经验要求|学历要求|招聘人数|发布时间|
        :return:
        """
        try:
            item = QcwyItem()
            item['position'] = response.xpath('//div[@class="cn"]//h1/text()').extract()[0].strip()
            item['salary'] = response.xpath('//div[@class="cn"]//strong/text()').extract_first()
            item['city'] = response.xpath('//div[@class="cn"]//p[contains(@class, "msg")]//text()').extract()[0].strip()
            item['experience'] = response.xpath('//div[@class="cn"]//p[contains(@class, "msg")]//text()').extract()[
                2].strip()
            item['education'] = response.xpath('//div[@class="cn"]//p[contains(@class, "msg")]//text()').extract()[
                4].strip()
            item['rec_number'] = response.xpath('//div[@class="cn"]//p[contains(@class, "msg")]//text()').extract()[
                6].strip()
            receive = response.css('.tCompany_center.clearfix > .tCompany_main > div:nth-child(1) > div p::text').extract()
            # 获取职位描述及技能要求部分信息，用于生成词云。（去掉其中的\xa0(&nbsp),\r,\n,\t）
            requirement_data = [
                each.strip().replace('\xa0', '') for each in receive if each.strip().replace('\xa0', '') != '']
            item['requirement'] = requirement_data
            yield item
        except:
            logger.debug('侦测到公司自定页面，非标准详情页，弃之！')


