'''Tests for Rrecipe APIs'''
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Recipe
from recipe.serializers import RecipeSerializer

RECIPE_URL = reverse("recipe:recipe-list")


def create_recipe(user, **params):
    '''Create Recipes helper function'''
    default = {
        'user': user,
        'title': "Sample Recipe",
        'time_minutes': 22,
        'price': Decimal("5.25"),
        'description': 'Sample Description',
        'link': 'https://example.com/recipe.pdf',
    }
    default.update(params)
    recipe = Recipe.objects.create(**default)


class PublicRecipeAPITest(TestCase):
    '''Public Tests for Recipe API'''

    def setUp(self):
        self.client = APIClient()

    def test_for_unauthorized_check(self):
        '''Test for unauthorized access to Recipe API'''
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITest(TestCase):
    '''Private testcases on Recipe API'''

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123',
        )
        self.client.force_login(user=self.user)

    def test_retireve_recipe_api(self):
        '''Test for Retrieve Recipe API'''
        create_recipe(user=self.user)
        create_recipe(user=self.user)
        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_recipe_api_limited_to_user(self):
        '''Test for limited retrieval for authenticated user'''
        other_user = get_user_model().objects.create_user(
            email='other@example.com',
            password='otherpass123',
        )
        create_recipe(user=other_user)
        create_recipe(user=self.user)
        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.all().filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
