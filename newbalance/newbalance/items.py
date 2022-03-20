
from scrapy import Field
from scrapy.item import Item


class NewBalanceItem(Item):
    url = Field()
    sku = Field()
    site_sku = Field()
    color = Field()
    genre = Field()
    img_search_page = Field()
    price = Field()
    image_urls = Field()
    image_uris = Field()
    size = Field()
    in_stock = Field()
    qty_stock = Field()
    spider = Field()
    spider_version = Field()
    timestamp = Field()
