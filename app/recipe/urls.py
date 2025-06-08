'''URLs for recipe API'''
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from recipe import views

router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)
app_name = 'recipe'
urlpatterns = [
    path('', include(router.urls)),
]
