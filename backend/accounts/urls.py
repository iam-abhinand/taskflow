from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import SignupView, LoginView, MyProfileView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login-refresh'),
    path('my-profile/', MyProfileView.as_view(), name='my-profile'),
]