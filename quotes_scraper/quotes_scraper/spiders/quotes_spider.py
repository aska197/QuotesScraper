import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            quote_text = quote.xpath("span[@class='text']/text()").get().strip('“”')
            quote_item = {
                "tags": quote.xpath("div[@class='tags']/a[@class='tag']/text()").extract(),
                "author": quote.xpath("span/small[@class='author']/text()").get(),
                "quote": f"“{quote_text}”"
            }
            yield quote_item

            author_url = quote.xpath("span/a/@href").get()
            if author_url is not None:
                yield response.follow(author_url, self.parse_author)

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield response.follow(next_link, self.parse)

    def parse_author(self, response):
        fullname = response.xpath("//h3[@class='author-title']/text()").get().strip()
        born_date = response.xpath("//span[@class='author-born-date']/text()").get().strip()
        born_location = response.xpath("//span[@class='author-born-location']/text()").get().strip()
        description = response.xpath("//div[@class='author-description']/text()").get().strip()
        
        author_item = {
            "fullname": fullname,
            "born_date": born_date,
            "born_location": born_location,
            "description": description
        }
        yield author_item
