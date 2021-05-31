from scrapy.crawler import  CrawlerProcess
from scrapy.settings import Settings

from hh_parse import settings
from hh_parse.spiders.hh_parse import Hh_parser

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(Hh_parser)
    process.start()