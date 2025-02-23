from django.urls import path
from .views import RegisterCompanyView, LoginView

urlpatterns = [
    path('register/', RegisterCompanyView.as_view(), name='register-company'), # Endpoint for company registration
    path('login/', LoginView.as_view(), name='login') # Endpoint for user login
]
