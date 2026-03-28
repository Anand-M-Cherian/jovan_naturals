"""Tests for store views."""

from django.test import TestCase


class ProductListViewTests(TestCase):
    """Tests for the product list (homepage) view."""

    def setUp(self):
        self.response = self.client.get("/")

    def test_product_list_returns_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_product_list_uses_correct_template(self):
        self.assertTemplateUsed(self.response, "store/product_list.html")

    def test_page_contains_hero_carousel(self):
        self.assertContains(self.response, "data-carousel")

    def test_page_contains_four_product_cards(self):
        self.assertEqual(self.response.content.count(b"data-product-card"), 4)

    def test_page_contains_bottom_nav(self):
        self.assertContains(self.response, 'data-nav="bottom"')
