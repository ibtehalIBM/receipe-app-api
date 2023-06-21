"""Tests for recipe."""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


from core.models import Recipe
from recipe.serializers import RecipeSerializer

from decimal import Decimal
RECIPE_URL = reverse('recipe:recipe-list')

def create_recipe(user, **params):
    """Create and Return a sample recipe."""
    defaults = {
        'title': 'Sample recipe title',
        'time_minutes': 22,
        'price': Decimal('5.25'),
        'description': 'Sample Description',
        'link': 'http://example.com/recipe.pdf'
    }

    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe

class PublicRecipeAPITests(TestCase):
    """Test unauthorixed API requests."""

    def setUp(self):

        self.user = get_user_model().objects.create(
            email = 'test@example.com',
            password = 'testpass123',
            name = 'Test Name'
        )

        self.client = APIClient()
        self.client.force_authenticate(user = self.user)

    def test_auth_required(self):
        """Test Authentication is required to call the API."""
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_recipes(self):

        create_recipe(user=self.user)
        create_recipe(user=self.user)
        res = self.client.get(RECIPE_URL)
        Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(res, many =True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """test list recipes is limited to authenticated user."""
        other_user = get_user_model().objects.create(
            email = 'otheruser@example.com',
            password = 'testpass123',
            name = 'Test Name'
        )
        create_recipe(user=self.user)
        create_recipe(user=other_user)

        res = self.client.get(RECIPE_URL)
        serializer = RecipeSerializer(res, many =True)

        recipes = Recipe.objects().filter(user = self.user)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

        recipes = Recipe.objects().filter(user = other_user)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
