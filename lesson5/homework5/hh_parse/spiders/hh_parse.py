"""
Источник https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113
вакансии удаленной работы.

Задача: Обойти с точки входа все вакансии и собрать след данные:
1. название вакансии
2. оклад (строкой от до или просто сумма)
3. Описание вакансии
4. ключевые навыки - в виде списка названий
5. ссылка на автора вакансии

Перейти на страницу автора вакансии,
собрать данные:
1. Название
2. сайт ссылка (если есть)
3. сферы деятельности (списком)
4. Описание
Обойти и собрать все вакансии данного автора.

"""

import scrapy
#from scrapy.http import HtmlResponse
from ..items import HhParseItem
#from lesson5.homework5.hh_parser.hh_parser.items import HhParserItem


class Hh_parser(scrapy.Spider):
    name = "hh_parser"
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113']

    def parse(self, response, **kwargs):

        next_page = response.css('a.bloko-button::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacansy = response.css('div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)').extract()
        print()
        for link in vacansy:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse(self, response):
            name = response.xpath("//h1[@class='bloko-header-1']/text()").extract_first()
            salary = response.xpath("//span[@class='bloko-header-2 bloko-header-2_lite']/text()").getall()
            description = response.xpath("//div[@class='g-user-content']/text()").getall()
            skills = response.xpath("//span[@class='bloko-tag__section bloko-tag__section_text']/text()").getall()
            print()
            #print(name, salary)
            yield HhParseItem(name=name, salary=salary, description=description, skills=skills)