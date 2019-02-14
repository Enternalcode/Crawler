# -*- coding: utf-8 -*-
import pymongo
from scrapy.exceptions import DropItem
from qcwy.middlewares import logger
from qcwy.utils.ToolFunction import convert_salary, extract_city, extract_ExpNum, extract_recnum


class DataClearPipeline(object):
    @staticmethod
    def process_item(item, spider):
        """
        查看是否为python有关职位
        子链接下公司招聘总览包含有其他不相关职位
        """

        salary_list = convert_salary(item['salary'])  # extract_city返回字典，键名为salary
        if salary_list:  # 若为False说明是异常格式数据
            item['salary'] = salary_list['salary']  # 格式化薪酬数据； 标准：千/月 无单位
            item['city'] = extract_city(item['city'])  # 提取城市信息
            temp = extract_ExpNum(item['experience'])  # 提取工作经验要求
            if temp:
                item['experience'] = temp
            item['rec_number'] = extract_recnum(item['rec_number'])
            return item
        else:
            logger.warning('出现异常数据')
            return DropItem("抛弃异常数据")


# MongoDB数据库
class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod  # 依赖注入方式，通过crawler类对象拿到全局配置的每个信息，然后用来初始化上面的mongo_uri、mongo_db
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):  # Spider打开时调用，连接mongodb并初始化配置
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):  # 插入数据
        # __class__将item实例变量指向类，然后调用__name__类属性，通常情况为'__main__'
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):  # 当Spider关闭时，断开与数据库的连接
        self.client.close()
