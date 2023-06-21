"""
views for the recipe API.
"""

from rest_framework import generics
from recipe.serializers import RecipeSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    """Create a new user in the system."""
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_query_set(self):
        """Retrieve recipe for authenticated users."""
        return self.queryset.filter(user=self.request.user).order_by('-id')