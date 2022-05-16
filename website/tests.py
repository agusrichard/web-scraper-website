from unittest import mock
from django.test import TestCase
from django.db import IntegrityError
from django.utils import timezone as tz

from website.tasks import scrape_website
from website.scheduler import scraping_scheduler
from website.models import ScrapingHistory, Article


class TestScrapingHistory(TestCase):
    def test_create_scraping_history(self):
        sh = ScrapingHistory()
        sh.save()
        self.assertEqual(sh.status, 0)
        self.assertEqual(sh.end_datetime, None)

        return sh

    def test_update_scraping_history_end_datetime(self):
        sh = self.test_create_scraping_history()

        sh.end_datetime = tz.now()
        diff = abs((tz.now() - sh.end_datetime).seconds)
        sh.save()

        self.assertAlmostEqual(diff, 0)

        return sh

    def test_update_scraping_history_change_status(self):
        sh = self.test_update_scraping_history_end_datetime()
        sh.status = 2
        sh.save()

        self.assertEqual(sh.status, 2)

        return sh

    def test_assert_scraping_history_str(self):
        sh = self.test_update_scraping_history_change_status()

        self.assertEqual(str(sh), "2")


class TestArticle(TestCase):
    def setUp(self):
        sh = ScrapingHistory()
        sh.save()

        self.scraping_history = sh

    def test_create_article(self):
        data = {
            "title": "Title",
            "author": "Author",
            "image_src": "https://image_src.com",
            "url": "https://url.com",
            "scraping_history": self.scraping_history,
            "published_date": tz.now(),
        }
        article = Article(**data)
        article.save()

        self.assertEqual(article.title, "Title")
        self.assertEqual(article.author, "Author")
        self.assertEqual(article.image_src, "https://image_src.com")
        self.assertEqual(article.url, "https://url.com")
        self.assertEqual(article.scraping_history, self.scraping_history)

        diff = abs((tz.now() - article.published_date).seconds)
        self.assertAlmostEqual(diff, 0)

        return data, article

    def test_handle_article_non_unique(self):
        data, article = self.test_create_article()

        with self.assertRaises(IntegrityError):
            article = Article(**data)
            article.save()

    def test_assert_article_str(self):
        _, article = self.test_create_article()

        self.assertEqual(str(article), "Title")


class TestMocked(TestCase):
    @mock.patch("website.scheduler.scrape_website")
    def test_scraping_scheduler(self, mocked_scrape_website):
        mocked_scrape_website.delay = mock.Mock()
        scraping_scheduler()
        mocked_scrape_website.delay.assert_called_once()

    @mock.patch("website.tasks.make_scraper")
    def test_scrape_website(self, mocked_make_scraper):
        mocked_make_scraper.return_value.__enter__.return_value.go_to_first_page = (
            mock.Mock()
        )
        mocked_make_scraper.return_value.__enter__.return_value.scroll_down = (
            mock.Mock()
        )

        scrape_website()

        mocked_make_scraper.return_value.__enter__.return_value.go_to_first_page.assert_called_once()
        mocked_make_scraper.return_value.__enter__.return_value.scroll_down.assert_called_once()


class TestViews(TestCase):
    def setUp(self) -> None:
        self.home_template = "website/home.html"
        self.scraping_history_template = "website/scraping_history.html"

    def assert_home(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.home_template)
        self.assertEqual(response.context["page_title"], "Home")

    def test_home(self):
        response = self.client.get("/")
        self.assert_home(response)

    def test_handle_home_query_strings_non_integer(self):
        response = self.client.get("/?page=word")
        self.assert_home(response)

    def test_handle_home_query_strings_page_out_of_range(self):
        response = self.client.get("/?page=100")
        self.assert_home(response)

    def assert_scraping_history(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.scraping_history_template)
        self.assertEqual(response.context["page_title"], "Scraping History")

    def test_scraping_history(self):
        response = self.client.get("/scraping-history/")
        self.assert_scraping_history(response)

    def test_handle_scraping_history_query_strings_non_integer(self):
        response = self.client.get("/scraping-history/?page=word")
        self.assert_scraping_history(response)

    def test_handle_scraping_history_uery_strings_page_out_of_range(self):
        response = self.client.get("/scraping-history/?page=100")
        self.assert_scraping_history(response)

    @mock.patch("website.views.scrape_website")
    def test_scrape_website(self, mocked_scrape_website):
        mocked_scrape_website.delay = mock.Mock()
        response = self.client.post("/run-manual-scraping/")
        mocked_scrape_website.delay.assert_called_once()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/scraping-history/")
