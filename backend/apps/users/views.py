from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated 
from .serializers import (
    RegisterSerializer,
    CustomTokenSerializer,
    UserSerializer,
    ProfileSerializer,
    PasswordChangeSerializer,
)
from django.contrib.auth import get_user_model
from rest_framework.response import Response 
from rest_framework import status   

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/me/        -> infos user
    PUT/PATCH /api/me/   -> maj partielle ou complète
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class PasswordChangeView(generics.UpdateAPIView):
    serializer_class   = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Mot de passe mis à jour"},
                        status=status.HTTP_200_OK)
