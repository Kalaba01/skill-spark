from django.urls import path
from .views import EmployeeListCreateView, EmployeeDetailView, UserListCreateView, UserDetailView

urlpatterns = [
    # Employee management routes (company)
    path("employees/", EmployeeListCreateView.as_view(), name="employee-list"),
    path("employees/<int:pk>/", EmployeeDetailView.as_view(), name="employee-detail"),

    # User management routes (admin)
    path("users/", UserListCreateView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail")
]
