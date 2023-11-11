import scrapy

class EbookSpider(scrapy.Spider):
    name = 'ebook'

    start_urls = [ "https://books.toscrape.com/" ]

    # def parse(self, response):
    #     print("[ parse ]")

    #     ebooks = response.css("article")

    #     for ebook in ebooks:
    #         title = ebook.css("a::text").get()
    #         price = ebook.css("p.price_color::text").get()

    #         yield {
    #             "title": title,
    #             "price": price
    #         }

    def parse(self, response):
        print("[ parse ]")

        # print(response.css("#messages").get())
        # print(response.css("a[title]").get())
        # print(response.xpath("//h3/a/text()").get()) # A Light in the Attic
        # print(response.xpath("//a[@title]").get()) # <a href="catalogue/a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in the ...</a>

        title = response.css("h3 a::attr(title)").get()
        price = response.xpath("//p[@class = 'price_color']").get()