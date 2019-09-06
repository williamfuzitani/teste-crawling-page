import scrapy

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
        SPEC_SELECTOR = response.xpath(
            "//table[contains(.//text(), 'Name')]//tr")
        IMAGE_SELECTOR = response.xpath("//*[@id='model-image']").xpath("@style").re('background-image: (url\((.*)\))')[1]
        BRAND_SELECTOR = response.xpath("//tr[contains(.//text(), 'Brand')]")
        MODEL_SELECTOR = response.xpath("//tr[contains(.//text(), 'Model')]")
        TRIM_SELECTOR = response.xpath("//tr[contains(.//text(), 'Trim')]")
        YEAR_SELECTOR = response.xpath(
            "//tr[contains(.//text(), 'Model year')]")

        for spec in SPEC_SELECTOR[1:]:
            yield {
                'BRAND': BRAND_SELECTOR.css('td:not(:first-child) ::text').get(),
                'MODEL': MODEL_SELECTOR.css('td:not(:first-child) ::text').get(),
                'TRIM': TRIM_SELECTOR.css('td:not(:first-child) ::text').get(),
                'YEAR': YEAR_SELECTOR.css('td:not(:first-child) ::text').get(),
                'IMAGE LINK': IMAGE_SELECTOR,

                'NAME': spec.css('td ::text')[0].get(),
                'INTERFACE': spec.css('td ::text')[1].get(),
                'POWER': spec.css('td ::text')[2].get(),
                'CURRENT': spec.css('td ::text')[3].get()
            }

        # yield {
        #     'brand': BRAND_SELECTOR.css('td:not(:first-child) ::text').get(),
        #     'model': MODEL_SELECTOR.css('td:not(:first-child) ::text').get(),
        #     'trim': TRIM_SELECTOR.css('td:not(:first-child) ::text').get(),
        #     'year': YEAR_SELECTOR.css('td:not(:first-child) ::text').get(),

        #     'name': SPEC_SELECTOR.css('td ::text')[0].get(),
        #     'interface': SPEC_SELECTOR.css('td ::text')[1].get(),
        #     'power': SPEC_SELECTOR.css('td ::text')[2].get(),
        #     'current': SPEC_SELECTOR.css('td ::text')[3].get()
        # }
