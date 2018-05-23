# coding=utf-8
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from WebCrawlers.items import NewsItem
import sys
import os

class NewsSpider(CrawlSpider):
    name = "news"
    basePath = '/home/mig/WebCrawlers/WebCrawlers/'
    allowed_domains = ["ycombinator.com"]
    start_urls = [
        "https://news.ycombinator.com/"
    ]
    rules = (
        Rule(
            LinkExtractor(allow="news.ycombinator.com/newest"),
            callback="parse_item",
            follow=True
        ),
    )
    maxItems = 3
    count = 0
    print("Starting spider: " + name + ". Item limit: " + str(maxItems))
    articlePath = basePath + 'NewsArticles/'
    if not os.path.exists(articlePath):
        os.makedirs(articlePath)

    """
Usa XPath para obtener una lista de los artículos en la página. Cada artículo está en un elemento de fila de tabla con una clase de "athing". Podemos tomar una secuencia de cada elemento coincidente de la siguiente manera:
    """
    def parse_item(self, response):
        print("Crawling: " + str(response.url) + "\n")
        articles = response.xpath('//tr[@class="athing"]')
        for article in articles:
            item = NewsItem()
            item["link_title"] = article.xpath('td[@class="title"]/a/text()').extract()[0]
            item["url"] = article.xpath('td[@class="title"]/a/@href').extract()[0]
            print("Extracting from: " + str(item["url"]))
            yield item
            self.on_item_parse()


    def on_item_parse(self):
        self.count += 1
        print("Items parsed: " + str(self.count) + "\n")
        if (self.count == self.maxItems):
            print("Spider: Item parse limit reached. Shutting down.")
            sys.exit("Exiting now.")