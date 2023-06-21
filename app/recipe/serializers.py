"""serializers for the recipe API views."""

from django.contrib.auth import (
    get_user_model,
    authenticate,
    )
from rest_framework import serializers
from django.utils.translation import gettext as _
from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = Recipe
        fields = ['id','description', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']