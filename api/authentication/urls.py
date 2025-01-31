from django.urls import path
from .views import RegisterCompanyView, LoginView

urlpatterns = [
    path('register/', RegisterCompanyView.as_view(), name='register-company'),
    path('login/', LoginView.as_view(), name='login')
]
