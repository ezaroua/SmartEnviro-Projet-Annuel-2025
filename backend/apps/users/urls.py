from django.urls import path
from .views import RegisterView, LoginView, MeView, ProfileView, PasswordChangeView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/',    LoginView.as_view(),    name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', ProfileView.as_view()),  
    path('change-password/', PasswordChangeView.as_view()),
]
