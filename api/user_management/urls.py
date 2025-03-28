from django.urls import path
from .views import (
    EmployeeListCreateView, 
    EmployeeDetailView, 
    EmployeeProfileView,
    UserListCreateView, 
    UserDetailView, 
    GenerateEmployeeReportView,
    CompanyProfileView
)

urlpatterns = [
    # Employee management routes (company)
    path("employees/", EmployeeListCreateView.as_view(), name="employee-list"),
    path("employees/<int:pk>/", EmployeeDetailView.as_view(), name="employee-detail"),
    path("employees/<int:pk>/report/", GenerateEmployeeReportView.as_view(), name="employee-report"),

    # User management routes (admin)
    path("users/", UserListCreateView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),

    # Employee profile route
    path("employee-profile/", EmployeeProfileView.as_view(), name="employee-profile"),

    # Company profile route
    path("company-profile/", CompanyProfileView.as_view(), name="company-profile")
]
