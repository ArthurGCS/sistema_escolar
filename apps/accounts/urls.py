from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UnidadeEscolarListView, RegisterView, LoginView, UserProfileView,
    ChangePasswordView, logout_view, UnidadeEscolarDetailView
)
from .views_templates import (
    login_view, register_view, logout_view_template, profile_view, change_password_view
)

app_name = 'accounts'

urlpatterns = [
    # API Endpoints
    path('api/unidades/', UnidadeEscolarListView.as_view(), name='unidades-list'),
    path('api/unidades/<int:pk>/', UnidadeEscolarDetailView.as_view(), name='unidade-detail'),
    path('api/register/', RegisterView.as_view(), name='api-register'),
    path('api/login/', LoginView.as_view(), name='api-login'),
    path('api/logout/', logout_view, name='api-logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/profile/', UserProfileView.as_view(), name='api-profile'),
    path('api/change-password/', ChangePasswordView.as_view(), name='api-change-password'),
    
    # Template Views
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view_template, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('change-password/', change_password_view, name='change-password'),
]
