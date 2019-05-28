# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from boss.items import BossItem



class ZhipinSpider(CrawlSpider):
    name = 'zhipin'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/c101280600/?query=python&page=1']

    rules = (
        Rule(LinkExtractor(allow=r'.+/?query=python&page=\d'), follow=True),
        Rule(LinkExtractor(allow=r'.+job_detail/[0-9a-zA-z-~]+.html'), callback="parse_job", follow=False),
    )

    def parse_job(self, response):

        name = response.xpath('//div[@class="name"]/h1/text()').get().strip()
        salary = response.xpath('//div[@class="name"]/span/text()').get().strip()
        job_info = response.xpath('//div[@class="job-primary detail-box"]/div[@class="info-primary"]/p/text()').getall()
        city = job_info[0]
        work_years = job_info[1]
        education = job_info[2]
        company = response.xpath('//div[@class="company-info"]/a/text()')[2].get().strip()
        # print(name,salary,job_info,city,work_years,education,company)

        item = BossItem(name=name,salary=salary,city=city,work_years=work_years,education=education,company=company)

        return item
