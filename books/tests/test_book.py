import unittest
from pathlib import Path

from books.items import BooksItem
from books.spiders.book import BookSpider
#模擬 Scrapy 下載完網頁後產生的 response，不用真的發 HTTP 請求，以及Scrapy 的「下一頁請求」物件
from scrapy.http import HtmlResponse, Request


def _get_sample_html_content():
    html_file_path = Path(__file__).parent / "sample.html"
    return html_file_path.read_text("utf-8")


class BookSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = BookSpider()
        self.example_html = _get_sample_html_content()
        self.response = HtmlResponse(
            url="https://books.toscrape.com",
            body=self.example_html,
            encoding="utf-8",
        )

    def test_parse_scrapes_all_items(self):#test_ 開頭 → unittest 才會執行
        """Test if the spider scrapes all books and pagination links."""
        # Collect the items produced by the generator in a list
        # so that it's possible to iterate over it more than once.
        #呼叫你的 spider 的 parse並且把所有 yield 的東西收集起來
        # [BooksItem(...),BooksItem(...),Request(...)]
        results = list(self.spider.parse(self.response))

        # There should be two book items and one pagination request
        #把 BooksItem 挑出來
        book_items = [item for item in results if isinstance(item, BooksItem)]
        #把分頁 Request 挑出來
        pagination_requests = [
            item for item in results if isinstance(item, Request)
        ]

        self.assertEqual(len(book_items), 2)
        self.assertEqual(len(pagination_requests), 1)

    def test_parse_scrapes_correct_book_information(self):
        """Test if the spider scrapes the correct information for each book."""
        results_generator = self.spider.parse(self.response)#generator會按順序產生

        # Book 1
        book_1 = next(results_generator)#抓第一筆generator資料
        self.assertEqual(
            book_1["url"], "catalogue/a-light-in-the-attic_1000/index.html"
        )
        self.assertEqual(book_1["title"], "A Light in the Attic")
        self.assertEqual(book_1["price"], "£51.77")

        # Book 2
        book_2 = next(results_generator)#抓第二筆generator資料
        self.assertEqual(
            book_2["url"], "catalogue/tipping-the-velvet_999/index.html"
        )
        self.assertEqual(book_2["title"], "Tipping the Velvet")
        self.assertEqual(book_2["price"], "£53.74")

    def test_parse_creates_pagination_request(self):
        """Test if the spider creates a pagination request correctly."""
        results = list(self.spider.parse(self.response))
        next_page_request = results[-1]
        self.assertIsInstance(next_page_request, Request)
        self.assertEqual(
            next_page_request.url,
            "https://books.toscrape.com/catalogue/page-2.html",
        )


if __name__ == "__main__":
    unittest.main()