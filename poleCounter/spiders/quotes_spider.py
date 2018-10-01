import scrapy


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
                i+=1
    def parse(self, response):
        yield{
            'username' :response.css('a[class=bigusername]::text')[1].extract(),
            'text' : response.xpath("(.//td[contains(@id,'td_post_')])[2]/text()").extract(),
            'thread' :response.request.url 
        }
