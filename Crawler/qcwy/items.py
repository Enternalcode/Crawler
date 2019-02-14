# -*- coding: utf-8 -*-
from scrapy import Item, Field


class QcwyItem(Item):
    """
    目标信息: 职位名称|薪酬水平|城市|经验要求|学历要求|招聘人数|职位要求|
    """
    position = Field()
    salary = Field()
    city = Field()
    experience = Field()
    education = Field()
    rec_number = Field()
    requirement = Field()