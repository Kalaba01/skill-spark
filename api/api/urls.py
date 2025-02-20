from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path("api/user-management/", include("user_management.urls")),
    path("api/password-reset/", include("password_reset.urls")),
    path("api/quizzes/", include("quizzes.urls")),
    path("api/dashboard/", include("dashboard.urls"))
]
