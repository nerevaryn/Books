import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from ..items import BooksItem


class BooksSpider(scrapy.Spider):
    name = 'books'
    base_url = ['http://books.toscrape.com/catalogue/']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        categories = response.xpath('//div[@class="side_categories"]//ul/li/ul/li/a')
        for category in categories:
            current_category = category.xpath('text()').get().strip()
            category = category.xpath('@href').get()
            absolute_url = response.urljoin(category)
            yield Request(absolute_url, callback=self.parse_categories, meta={'current_category': current_category})


    def parse_categories(self, response):
        field_categories = 'books'
        current_category = response.meta['current_category']
        field_categories = field_categories + ' > ' + current_category
        results_amount = response.xpath('//form[@method="get"]/div//following-sibling::strong/text()').get()
        product_links = response.xpath('//h3/a/@href').getall()
        for product_link in product_links:
            absolute_product_link = response.urljoin(product_link)
            yield Request(absolute_product_link, callback=self.parse_product,
                          meta={'field_categories': field_categories, 'product_url': absolute_product_link,
                                'results_amount': results_amount})

        next_page_url = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page_url:
            absolute_next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=absolute_next_page_url, callback=self.parse_categories, meta={'next_page_request': True})


    def parse_product(self, response):
        l = ItemLoader(item=BooksItem(), response=response)
        categories = response.meta['field_categories']
        results_amount = response.meta['results_amount']
        url = response.meta['product_url']
        image_path = response.xpath('//div[@class="item active"]/img/@src').get().strip(),
        image_path = image_path[0].replace('../..', 'http://books.toscrape.com/'),
        title = response.xpath('//div[@class="col-sm-6 product_main"]//h1/text()').get(),
        price = response.xpath('//p[@class="price_color"]/text()').get().strip(),
        upc = response.xpath('//tr[1]/td/text()').get().strip(),
        availability = response.xpath('//tr[6]/td/text()').get().strip(),

        try:
            description = response.xpath('//article[@class="product_page"]/p/text()').get().strip(),
        except AttributeError:
            description = ''
        l.add_value('title', title),
        l.add_value('price', price),
        l.add_value('upc', upc)
        l.add_value('availability', availability),
        l.add_value('description', description),
        l.add_value('category', categories),
        l.add_value('results_amount', results_amount),
        l.add_value('url', url),
        l.add_value('image', image_path),
        return l.load_item()
