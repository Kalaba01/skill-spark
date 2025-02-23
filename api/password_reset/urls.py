from django.urls import path
from .views import RequestPasswordResetView, PasswordResetConfirmView

urlpatterns = [
    path("", RequestPasswordResetView.as_view(), name="password_reset"), # Endpoint for requesting a password reset link
    path("confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm") # Endpoint for confirming password reset using the provided token
]
