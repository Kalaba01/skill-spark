from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), # Django Admin Panel
    path('api/auth/', include('authentication.urls')), # Authentication API
    path("api/user-management/", include("user_management.urls")), # User Management API
    path("api/password-reset/", include("password_reset.urls")), # Password Reset API
    path("api/quizzes/", include("quizzes.urls")), # Quizzes API
    path("api/dashboard/", include("dashboard.urls")) # Dashboard API
]
