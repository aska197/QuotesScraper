import os
import json
import scrapy
from scrapy.crawler import CrawlerProcess

# Define the relative path for data folder
data_folder = 'quotes_scraper/data'

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    custom_settings = {
        'FEEDS': {
            os.path.join(data_folder, 'quotes.json'): {
                'format': 'json',
                'overwrite': True,
                'encoding': 'utf8',
                'indent': 4
            }
        }
    }

    authors_seen = set()
    authors_data = []

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
        if fullname not in self.authors_seen:
            self.authors_seen.add(fullname)
            born_date = response.xpath("//span[@class='author-born-date']/text()").get().strip()
            born_location = response.xpath("//span[@class='author-born-location']/text()").get().strip()
            description = response.xpath("//div[@class='author-description']/text()").get().strip()

            author_item = {
                "fullname": fullname,
                "born_date": born_date,
                "born_location": born_location,
                "description": description
            }
            self.authors_data.append(author_item)

    def closed(self, reason):
        authors_file = os.path.join(data_folder, 'authors.json')
        with open(authors_file, 'w', encoding='utf8') as f:
            json.dump(self.authors_data, f, ensure_ascii=False, indent=4)


def clear_json_files():
    json_files = [
        os.path.join(data_folder, 'quotes.json'),
        os.path.join(data_folder, 'authors.json')
    ]

    for file in json_files:
        if os.path.exists(file):
            with open(file, 'w') as f:
                f.write('')
        else:
            os.makedirs(os.path.dirname(file), exist_ok=True)
            with open(file, 'w') as f:
                pass


def run_crawler():
    clear_json_files()

    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()


if __name__ == "__main__":
    run_crawler()
