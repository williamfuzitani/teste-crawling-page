# response.css('div.brand-listing-container-frontpage a').getall()
import scrapy

# class Car(scrap.Item):
#     brand = scrapy.Field()
#     model = scrapy.Field()
#     year = scrapy.Field()

class BrickSetSpider(scrapy.Spider):
    name = "ev"
    start_urls = ['https://www.evspecifications.com/']

    def parse(self, response):
        SET_SELECTOR = response.css('div.brand-listing-container-frontpage a')

        for brand in SET_SELECTOR:
            NAME_SELECTOR = 'a ::text'
            PAGE_SELECTOR = 'a ::attr(href)'
            brand_page = brand.css(PAGE_SELECTOR).extract_first()
            # yield {
            #     'brand name': brand.css(NAME_SELECTOR).extract_first(),
            #     'brand link': brand.css(PAGE_SELECTOR).extract_first()
            # }

            if brand_page:
                yield scrapy.Request(
                    response.urljoin(brand_page),
                    callback=self.parse_cars
                )

    def parse_cars(self, response):
        CAR_SELECTOR = response.css('div.model-listing-container-80 div h3 a')

        for brand_car in CAR_SELECTOR:
            CAR_NAME_SELECTOR = 'a ::text'
            CAR_PAGE_SELECTOR = 'a ::attr(href)'
            car_page = brand_car.css(CAR_PAGE_SELECTOR).extract_first()
            # yield {
            #     'car name': brand_car.css(CAR_NAME_SELECTOR).extract_first(),
            #     'car link': brand_car.css(CAR_PAGE_SELECTOR).extract_first()
            # }

            if car_page:
                yield scrapy.Request(
                    response.urljoin(car_page),
                    callback=self.parse_specs
                )

    def parse_specs(self, response):
        SPEC_SELECTOR = response.xpath('/html/body/div[3]/div[4]/table[1]')
        yield {
            'brand': SPEC_SELECTOR.xpath('tr[1]/td[2]//text()').get(),
            'model': SPEC_SELECTOR.xpath('tr[2]/td[2]//text()').get(),
            'year': SPEC_SELECTOR.xpath('tr[4]/td[2]//text()').get()
        }


        # for spec_car in SPEC_SELECTOR[0:]:
        #     BRAND = 'tr td ::text'
        #     MODEL = 'tr td ::text'
        #     YEAR = 'tr td ::text'
        #     yield {
        #         'brand': spec_car.css(BRAND).get(),
        #         'model': spec_car.css(MODEL).get(),
        #         'year': spec_car.css(YEAR).get()
        #     }