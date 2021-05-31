"""
Источник https://auto.youla.ru/
Обойти все марки авто и зайти на странички объявлений
Собрать след стуркутру и сохранить в БД Монго
Название объявления
Список фото объявления (ссылки)
Список характеристик
Описание объявления
ссылка на автора объявления
дополнительно попробуйте вытащить телефона
"""

import scrapy
from gb_parse.items import GbParseItem


class AutoyoulaSpider(scrapy.Spider):
    name = "autoyoula"
    allowed_domains = ["auto.youla.ru"]
    start_urls = ["https://auto.youla.ru/"]

    def _get_follow(self, response, select_str, callback, **kwargs):
        for a in response.css(select_str):
            url = a.attrib.get("href")
            yield response.follow(url, callback=callback, **kwargs)

    def parse(self, response):
        print()
        yield from self._get_follow(
            response, "div.TransportMainFilters_brandsList__2tIkv a.blackLink", self.brand_parse
        )

    def brand_parse(self, response):
        yield from self._get_follow(
            response, "div.Paginator_block__2XAPy a.Paginator_button__u1e7D", self.brand_parse
        )
        yield from self._get_follow(
            response,
            "article.SerpSnippet_snippet__3O1t2 a.SerpSnippet_name__3F7Yu",
            self.car_parse,
        )

    def car_parse(self, response):
        data = {
            "url": response.url,
            "title": response.css("div.AdvertCard_advertTitle__1S1Ak::text").extract_first(),
            "price": float(
                response.css("div.AdvertCard_price__3dDCr::text")
                .extract_first()
                .replace("\u2009", "")
            ),
            "photo": response.css("figure.PhotoGallery_photo__36e_r img").attrib.get("src"),
            "description": response.css(".AdvertCard_descriptionInner__KnuRi::text").extract_first(),
            "characteristics": {
                #year
                response.css(".AdvertSpecs_label__2JHnS::text").extract_first():
                    response.css("div.AdvertSpecs_row__ljPcX div.AdvertSpecs_data__xK2Qx::text").extract_first(),
                "Пробег": response.xpath('//div[@data-target="advert-info-mileage"]/text()').get(),
                "КПП": response.xpath('//div[@data-target="advert-info-transmission"]/text()').get(),
                "Двигатель": response.xpath('//div[@data-target="advert-info-engineInfo"]/text()').get(),
                "Руль": response.xpath('//div[@data-target="advert-info-wheelType"]/text()').get(),
                "Цвет": response.xpath('//div[@data-target="advert-info-color"]/text()').get(),
                "Привод": response.xpath('//div[@data-target="advert-info-driveType"]/text()').get(),
                "Мощность": response.xpath('//div[@data-target="advert-info-enginePower"]/text()').get(),
                "VIN": response.xpath('//div[@data-target="advert-info-vinCode"]/text()').get(),
                "Растаможен": response.xpath('//div[@data-target="advert-info-isCustom"]/text()').get(),
                "Владельцев": response.xpath('//div[@data-target="advert-info-owners"]/text()').get(),
                },


        }
        yield GbParseItem(title = data["title"], price=data["price"])  #data


