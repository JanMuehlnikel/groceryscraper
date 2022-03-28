import scrapy
from groceryscraper.items import ProductItem
from datetime import date


class QuotesSpider(scrapy.Spider):
    name = 'aldi'
    store_identifier = 'https://www.aldi-sued.de'
    start_urls = ['https://www.aldi-sued.de/de/produkte/produktsortiment.html']

    def parse(self, response):
        # Find out urls and store them in a list
        category_url_list = response.xpath("//a[@class='btn btn-primary small btn-minwidth_140']/@href").extract()

        # Iterate through the categories
        for link in category_url_list:
            url = self.store_identifier + link
            next_page = response.urljoin(url)

            yield scrapy.Request(
                next_page,
                callback=self.parse_categories,
                meta={'url': next_page,'page_number': 0}
            )

    def parse_categories(self, response):
        category_url = response.meta.get("url")
        category_name = response.xpath('//h1[@class="plp_title"]//text()').get().strip()
        page_number = response.meta.get("page_number")

        # Find out number of Products in this category
        products_num = int(response.xpath('//*[@id="productsNumber"]//text()').get().strip(' Produkte'))
        if products_num > 0 or page_number == 0:
            # Find out url to products to scrape the information and store them in a list
            category_page_products_urls = response.xpath('//*[@id="plpProducts"]/article/a/@href').extract()
            for url in category_page_products_urls:
                product_page = response.urljoin(self.store_identifier + url)

                yield scrapy.Request(product_page,
                                     callback=self.parse_product,
                                     meta={'name': category_name}
                                     )

            page_number += 1
            suffix_url = f'?pageNumber={page_number}&_1647262634865'
            product_page_url = category_url + suffix_url
            next_category_page = response.urljoin(product_page_url)

            yield scrapy.Request(next_category_page,
                                 callback=self.parse_categories,
                                 meta={'url': category_url, 'name': category_name, 'page_number': page_number})

        else:
            self.logger.debug("Parsing url: %s. Category: %s has finnished" % (category_name, category_url))

    def parse_product(self, response):

        category_name_str = response.meta.get("name")

        name_str = response.xpath(
            '//*[@id="pdpDetails"]/div[2]/div[3]/h1//text()').get().strip()

        price_str = response.xpath(
            '//*[@id="pdpDetails"]/div[2]/div[4]/div[1]/div/div[1]/span//text()')\
            .get().replace('€', '').replace(',', '.').strip()

        description_str = ''
        for i in range(1, 8):

            description = str(response.xpath(
                f'//*[@id="content-panel-1"]/section/div[1]/div/ul/li[{i}]//text()')
                                       .get()).strip()

            if description != 'None':
                description_str += description

        image = response.xpath(
            '//a[@class="active zoom-ico-image"]/@href').get().strip()

        date_str = date.today()

        item = ProductItem()
        item['name'] = name_str
        item['price'] = price_str
        item['description'] = description_str
        item['image'] = image
        item['category'] = category_name_str
        item['date'] = date_str
        item['store'] = 'aldi'

        yield item

