from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from gb_parse import settings
from gb_parse.spiders.autoyoula import AutoyoulaSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(AutoyoulaSpider)
    process.start()