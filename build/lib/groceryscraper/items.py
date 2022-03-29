import scrapy
from w3lib.html import remove_tags
from itemloaders.processors import TakeFirst, MapCompose
import scrapy


def remove_currency(value):
    return value.replace('€', '')


def strip(value):
    return value.replace('\t', '').replace('\n', '').replace(' ', '')


class ProductItem(scrapy.Item):
    description = scrapy.Field(input_processor=MapCompose(remove_tags, strip), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(remove_tags, strip), output_processor=TakeFirst())
    name = scrapy.Field(input_processor=MapCompose(remove_tags, strip), output_processor=TakeFirst())
    image = scrapy.Field(input_processor=MapCompose(remove_tags, strip), output_processor=TakeFirst())
    category = scrapy.Field(input_processor=MapCompose(remove_tags, strip), output_processor=TakeFirst())
    date = scrapy.Field(input_processor=MapCompose(remove_tags, strip), output_processor=TakeFirst())
    store = scrapy.Field(input_processor=MapCompose(remove_tags, strip), output_processor=TakeFirst())

    pass
