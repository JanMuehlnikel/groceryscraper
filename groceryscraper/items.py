import scrapy
from w3lib.html import remove_tags
from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader


def remove_currency(value):
    return value.replace('€', '')


def strip(value):
    return value.replace('\t', '').replace('\n', '').replace(' ', '')


class ProductItem(scrapy.Item):
    # define the fields for your item here like:
    description = scrapy.Field(input_processor=MapCompose(remove_tags, strip), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(remove_tags, strip), output_processor=TakeFirst())
    name = scrapy.Field(input_processor=MapCompose(remove_tags, strip), output_processor=TakeFirst())
    pass
