# Quotes Scraper and MongoDB Loader

## Overview

This project is designed to scrape quotes and author information from a website, store the data in JSON files, and then load this data into a MongoDB database. The project demonstrates the ability to extract and manage data efficiently, showcasing proficiency in web scraping, data parsing, and database integration.

## Installation

1. Clone the repository.
2. Install the required Python packages.
3. Set up MongoDB and ensure it's running.

## Usage

### Scraping Data

Run the Scrapy spider to scrape the quotes and author information:
```sh
python main_crawler.py
```
This will save the scraped quotes to `data/quotes.json` and author information to `data/authors.json`.

### Loading Data into MongoDB

Run the data loader script to load the scraped data into MongoDB:
```sh
python load_data.py
```

## File Details

### `main_crawler.py`

This script initializes and runs the Scrapy spider.

### `quotes_scraper/spiders/quotes_spider.py`

The Scrapy spider for scraping quotes and author information.

### `load_data.py`

This script reads the scraped data from JSON files and loads it into MongoDB.


## Conclusion

This project showcases the ability to build a complete data pipeline from web scraping to database storage, demonstrating proficiency in web scraping, data parsing, and database management.
