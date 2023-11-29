from typing import Any
import scrapy
from scrapy.http import Response

class ReviewSpider(scrapy.Spider):
    name = "review"

    start_urls = [ "https://www.booking.com/hotel/hk/regal.zh-cn.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaGKIAQGYASu4ARfIAQzYAQHoAQH4AQyIAgGoAgO4AtK456oGwAIB0gIkZjFlYzUwZGYtMDg3ZS00MTAwLTllYWUtMzYwMDY5OTc0MTM52AIG4AIB&sid=97fc0c71d1839a7dcfbd937dcaafc073&dest_id=55015;dest_type=hotel;dist=0;group_adults=2;group_children=0;hapos=1;hpos=1;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1700387862;srpvid=0ff44633530d0106;type=total;ucfs=1&#tab-reviews" ]
## review url:
## https://www.booking.com/hotel/hk/regal.zh-cn.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaGKIAQGYASu4ARfIAQzYAQHoAQH4AQyIAgGoAgO4AtK456oGwAIB0gIkZjFlYzUwZGYtMDg3ZS00MTAwLTllYWUtMzYwMDY5OTc0MTM52AIG4AIB&sid=97fc0c71d1839a7dcfbd937dcaafc073&dest_id=55015;dest_type=hotel;dist=0;group_adults=2;group_children=0;hapos=1;hpos=1;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1700387862;srpvid=0ff44633530d0106;type=total;ucfs=1&#tab-reviews

    def parse(self, response):
        print("[parse]")

        reviews = response.css("review_list_new_item_block")

        for review in reviews:
            comment = review.css("h3.c-review-block__title c-review__title--ltr::text").get()
            print(comment)