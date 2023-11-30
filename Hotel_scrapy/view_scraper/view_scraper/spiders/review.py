from typing import Any
import scrapy
from scrapy.http import Response

class ReviewSpider(scrapy.Spider):
    name = "review"

    start_urls = [ "https://www.booking.com/hotel/hk/regal.html?aid=304142&label=gen173nr-1FCA0oMkIRaWJpcy1ib2dvdGEtbXVzZW9IClgEaGKIAQGYAQq4ARfIAQzYAQHoAQH4AQOIAgGoAgO4As_DnasGwAIB0gIkZTNhNTIxMDQtNzYxYi00ZjNiLWFlZTktMTI4MmNjNmY4Mjhk2AIF4AIB&sid=31e68598118dc4d2d9106a5ac7af72d9&dest_id=55015;dest_type=hotel;dist=0;group_adults=2;group_children=0;hapos=1;hpos=1;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1701274067;srpvid=592e71ed50b0009f;type=total;ucfs=1&#tab-reviews" ]


    #start_urls= ["https://books.toscrape.com/"]
    # for testing the scrapy run normally

## review url:
## https://www.booking.com/hotel/hk/regal.zh-cn.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaGKIAQGYASu4ARfIAQzYAQHoAQH4AQyIAgGoAgO4AtK456oGwAIB0gIkZjFlYzUwZGYtMDg3ZS00MTAwLTllYWUtMzYwMDY5OTc0MTM52AIG4AIB&sid=97fc0c71d1839a7dcfbd937dcaafc073&dest_id=55015;dest_type=hotel;dist=0;group_adults=2;group_children=0;hapos=1;hpos=1;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1700387862;srpvid=0ff44633530d0106;type=total;ucfs=1&#tab-reviews

    def parse(self, response):
        print("[parse]")

        #reviews = response.xpath('//*[@id="review_list_page_container"]')
        reviews = response.xpath('//span[@class="bui-avatar-block__title"]/text()').get()
        #reviews = response.css("h3 a").get()
        # for testing the scrapy run normally

        # for review in reviews:
        #   comment = review.xpath('//*[@id="review_list_page_container"]//h3::text').get()
        #   print(comment)
        print(reviews)

