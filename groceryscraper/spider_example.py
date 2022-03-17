import scrapy
import csv
import math


class QuotesSpider(scrapy.Spider):
    name = 'example'
    prefix_url = 'https://www.aldi-sued.de'
    start_urls = ['https://www.aldi-sued.de/de/produkte/produktsortiment.html']

    def parse(self, response):
        # Find out number of categories
        number_of_categories = float(response.xpath(
            "count(//a[@class='btn btn-primary small btn-minwidth_140']/@href)"
        ).get())

        # Find out urls and store them in a list
        url_category_list = response.xpath(
            "//a[@class='btn btn-primary small btn-minwidth_140']/@href"
        ).extract()

        # Iterate through the categories
        for link in url_category_list:
            url = self.prefix_url + link

            next_page = response.urljoin(url)
            yield scrapy.Request(next_page, callback=self.parse_categories)

    def parse_categories(self, response):

        # Find out number of Products
        products_num = int(response.xpath('//*[@id="productsNumber"]//text()').get().strip(' Produkte'))

        # Find out all links to the category pages
        page_num = 1
        current_url = response.xpath("//link[@rel='canonical']/@href").get()
        rounds = math.ceil(products_num / 18)

        for i in range(1, rounds + 1):
            suffix_url = f'?pageNumber={page_num}&_1647262634865'
            product_page_url = current_url + suffix_url

            next_page = response.urljoin(product_page_url)
            page_num += 1

            yield scrapy.Request(next_page, callback=self.parse_category_sites)

    def parse_category_sites(self, response):

        # open the product pages
        product_urls = response.xpath('//*[@id="plpProducts"]/article/a/@href').extract()

        for product_url in product_urls:
            url = self.prefix_url + product_url

            next_page = response.urljoin(url)
            yield scrapy.Request(next_page, callback=self.parse_product_page)

    def parse_product_page(self, response):

        # Scrape product information
        product_information = []

        # Product Name
        product_name = response.xpath('//*[@id="pdpDetails"]/div[2]/div[3]/h1//text()').get()\
            .strip('\n')\
            .strip(' ')
        product_information.append(str(product_name))

        # Product Price
        product_price = response.xpath('//*[@id="pdpDetails"]/div[2]/div[4]/div[1]/div/div[1]/span//text()').get(). \
            strip('\t'). \
            strip(' '). \
            replace('\n', '').\
            replace('€', '')
        product_information.append(str(product_price))

        # Product Description
        product_description = ''
        for i in range(1, 8):

            description = str(response.xpath(
                f'//*[@id="content-panel-1"]/section/div[1]/div/ul/li[{i}]//text()')
                                       .get())

            if description != 'None':
                product_description += description

        product_information.append(str(product_description))

        # Write in csv
        with open('Products', 'a', encoding='utf8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(product_information)
