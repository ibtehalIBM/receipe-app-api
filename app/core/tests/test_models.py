"""
Tests for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models
from decimal import Decimal
class ModelTests(TestCase):
    """Test Models"""

    def test_create_user_with_email_successful(self):
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]
        for email, expected_email in sample_emails:
            user = get_user_model().objects.create_user(email)
            self.assertEqual(user.email, expected_email)

    def test_new_user_withour_email_raises_error(self):
        """
        Test Adding user without Email raises ValueError
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', '123')

    def test_create_super_user(self):
        """
        Test create a superuser.
        """
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test Creating a recipe is successful."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        recipe = models.Recipe.objects.create(
            user = user,
            title = 'Simple Recipe Name',
            time_minutes=5,
            price= Decimal('5.50'),
            description = 'Sample Recipe Description.',
        )

        self.assertEqual(str(recipe), recipe.title)