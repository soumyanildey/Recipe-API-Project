from rest_framework import generics, authentication, permissions
from .serializers import UserSerializer, AuthenticationSerializer
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken


class CreateUserView(generics.CreateAPIView):
    '''Viewset for handling the create user serializer'''
    serializer_class = UserSerializer


class CreateAuthToken(ObtainAuthToken):
    '''Creates auth token'''
    serializer_class = AuthenticationSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UpdateUserView(generics.RetrieveUpdateAPIView):
    '''Retrieve and Update user profile view'''
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        '''Retrieve and update current authenticated user'''
        return self.request.user
