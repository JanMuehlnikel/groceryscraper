import scrapy
from groceryscraper.items import ProductItem
from datetime import date


class QuotesSpider(scrapy.Spider):
    name = 'carrefour'
    handle_httpstatus_all = True
    store_identifier = 'https://www.jumia.ci/'
    start_urls = ['https://www.jumia.ci/mlp-boutique-carrefour/']

    def parse(self, response):
        category_list = response.xpath("//*[@id='ctlg']/div/div/section/div/a/@href").extract()
        print(category_list)

        for link in category_list:
            category_page_url = response.urljoin(f'{link}?page=1#catalog-listing')
            category_link = link

            yield scrapy.Request(category_page_url,
                                 callback=self.parse_category,
                                 meta={'link': category_link, 'page': 1}
                                 )

    def parse_category(self, response):
        category_link = response.meta.get('link')
        page = response.meta.get('page')
        category_name = response.xpath('//*[@id="jm"]/main/div[2]/div[2]/div/article[1]/a[1]//text()').get()

        if response.xpath("//*[@id='jm']/main/div[2]/div[3]/section/header/div[2]/p//text()").get() is not None:
            # Open product pages
            for i in range(1, 41):
                product_link = response.xpath(f"//*[@id='jm']/main/div[2]/div[3]/section/div[1]/article[{i}]/a/@href").get()
                url = self.store_identifier + product_link
                product_page_url = response.urljoin(url)

                yield scrapy.Request(product_page_url,
                                     callback=self.parse_product,
                                     meta={'name': category_name}
                                     )
            # Scrape next Category page
            page += 1
            url = f'{category_link}?page={page}#catalog-listing'
            category_page_url = response.urljoin(url)

            yield scrapy.Request(category_page_url,
                                 callback=self.parse_category,
                                 meta={'name': category_name, 'page': page}
                                 )

    def parse_product(self, response):
        category_name_str = response.meta.get('name')

        name_str = response.xpath(
            '//*[@id="jm"]/main/div[1]/section/div/div[2]/div[1]/div/h1//text()'
        ).get().strip()

        price_str = response.xpath(
            '//*[@id="jm"]/main/div[1]/section/div/div[2]/div[2]/div/div/span//text()'
        ).get().replace('FCFA', '').replace('.', '').strip()

        description_str = response.xpath(
            '//*[@id="jm"]/main/div[2]/div[2]/section[1]/div[2]/article[1]/div/div').get().strip()

        image = response.xpath(
            '//*[@id="imgs"]/a/@href').get().strip()

        date_str = date.today()

        item = ProductItem()
        item['name'] = name_str
        item['price'] = price_str
        item['description'] = description_str
        item['image'] = image
        item['category'] = category_name_str
        item['date'] = date_str
        item['store'] = 'carrefour_cote_divoire'

        yield item