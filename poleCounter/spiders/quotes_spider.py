import scrapy
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.poles
poles = db.poles
notCrawled = db.notCrawled


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://www.forocoches.com/foro/showthread.php?t='
        ]
        for url in urls:
            i = 1
            while True:
                yield scrapy.Request(url=url+str(i), callback=self.parse)
                i += 1

    def parse(self, response):
        try:
            data = {
                'username': response.css('a[class=bigusername]::text')[1].extract(),
                'text': response.xpath("(.//td[contains(@id,'td_post_')])[2]/text()").extract(),
                'thread': response.request.url
            }
            result = poles.insert_one(data)
        except IndexError:
            data = {
                'url': response.request.url
            }
            result = notCrawled.insert_one(data)
