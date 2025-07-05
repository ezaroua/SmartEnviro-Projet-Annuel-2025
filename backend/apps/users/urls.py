from django.urls import path
from .views import RegisterView, LoginView, MeView, ProfileView, PasswordChangeView, UserListView, UserDeleteView, UserToggleActiveView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/',    LoginView.as_view(),    name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', ProfileView.as_view()),  
    path('change-password/', PasswordChangeView.as_view()),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDeleteView.as_view(), name='user-delete'),
    path('users/<int:pk>/toggle_active/', UserToggleActiveView.as_view(), name='user-toggle-active'),

]
