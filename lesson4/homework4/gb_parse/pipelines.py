# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import pymongo


class GbParsePipeline(object):
    def __init__(self):
        client = pymongo.MongoClient("mongodb://localhost:27017") #db_client = pymongo.MongoClient("mongodb://localhost:27017")
        self.mongobase = client["autoyoula_7_04_21"]  #db = db_client["gb_data_mining_15_02_2021"]
        #self.collection = self.db["magnit_products"]
        #self.collection.insert_one(data)

    def process_item(self, item, spider):
        print(spider.name)
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        print(item['salary'])

        return item





