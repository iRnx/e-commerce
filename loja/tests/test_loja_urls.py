from django.test import TestCase
from django.urls import reverse


class RecipeUrlsTest(TestCase):

    def test_recipe_home_url_is_correct(self):
        url = reverse('loja:teste')
        self.assertEqual(url, '/')
