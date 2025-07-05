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
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model  
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


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
class UserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class UserToggleActiveView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.is_active = not user.is_active
            user.save()
            return Response({'success': True, 'is_active': user.is_active})
        except User.DoesNotExist:
            return Response({'error': 'Utilisateur non trouvé'}, status=status.HTTP_404_NOT_FOUND)
        
class AdminOverviewView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        today = timezone.now().date()
        last_7_days = [today - timedelta(days=i) for i in reversed(range(7))]
        weekly_counts = [
            User.objects.filter(date_joined__date=day).count() for day in last_7_days
        ]

        data = {
            "total_users": User.objects.count(),
            "admins": User.objects.filter(role__name='admin').count(),
            "citizens": User.objects.filter(role__name='citizen').count(),
            "active_users": User.objects.filter(is_active=True).count(),
            "inactive_users": User.objects.filter(is_active=False).count(),
            "weekly_registrations": weekly_counts,
            "last_users": list(User.objects.order_by('-date_joined')[:5].values(
                'id', 'username', 'email', 'date_joined'
            )),
        }
        return Response(data)