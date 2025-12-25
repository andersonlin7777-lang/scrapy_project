import scrapy
#要用BooksItem 來裝抓到的資料
from books.items import BooksItem

class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["books.toscrape.com"]#限制這隻 spider 只能抓這個網域
    start_urls = ["https://books.toscrape.com/"]

    def start_requests(self):#use .log_error() for the initial request to Books to Scrape
        for url in self.start_urls:
            yield scrapy.Request(
                url, callback=self.parse, errorback=self.log_error
            )

    def log_error(self, failure):
        self.logger.error(repr(failure))

    def parse(self, response):#response = 抓回來的 HTML 包裝物件
        for book in response.css("article.product_pod"):
            item = BooksItem()
            item["url"] = book.css("h3 > a::attr(href)").get()
            item["title"] = book.css("h3 > a::attr(title)").get()
            item["price"] = book.css(".price_color::text").get()
            yield item#把這一筆書籍資料「交給 Scrapy」 

        next_page = response.css("li.next > a::attr(href)").get()
        if next_page:
            next_page_url = response.urljoin(next_page)#把相對網址變成完整網址
            self.logger.info(
                f"navigating to next page with URL {next_page_url}"
            )
            #告訴 Scrapy：去抓 next_page_url抓回來後，再交給 parse() 處理一次
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse,
                errorback=self.log_error
            )
            
