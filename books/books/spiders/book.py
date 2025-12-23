import scrapy
#要用BooksItem 來裝抓到的資料
from books.items import BooksItem

class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["books.toscrape.com"]#限制這隻 spider 只能抓這個網域
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):#response = 抓回來的 HTML 包裝物件
        for book in response.css("article.product_pod"):
            item = BooksItem()
            item["url"] = book.css("h3 > a::attr(href)").get()
            item["title"] = book.css("h3 > a::attr(title)").get()
            item["price"] = book.css(".price_color::text").get()
            yield item#把這一筆書籍資料「交給 Scrapy」 
