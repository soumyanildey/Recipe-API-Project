from rest_framework import generics
from .serializers import UserSerializer

class CreateUserView(generics.CreateAPIView):
    '''Viewset for handling the create user serializer'''
    serializer_class = UserSerializer
