from django.urls import path
from .views import RegisterCompanyView

urlpatterns = [
    path('register/', RegisterCompanyView.as_view(), name='register-company')
]
