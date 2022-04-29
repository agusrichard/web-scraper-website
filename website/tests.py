from django.db import IntegrityError
from django.utils import timezone as tz
from django.test import TestCase

from .models import ScrapingHistory, Article


class ScrapingHistoryTests(TestCase):
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


class ArticleTests(TestCase):
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
