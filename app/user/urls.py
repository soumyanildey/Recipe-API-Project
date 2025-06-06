from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateAuthToken.as_view(), name='token'),
    path('me', views.UpdateUserView.as_view(), name='me'),
]
