from django.urls import path
from .views import AdminDashboardStatsView, CompanyDashboardStatsView, EmployeeDashboardStatsView

urlpatterns = [
    path("admin-dashboard/", AdminDashboardStatsView.as_view(), name="admin-dashboard-stats"), # Endpoint for retrieving admin dashboard statistics
    path("company-dashboard/", CompanyDashboardStatsView.as_view(), name="company-dashboard-stats"), # Endpoint for retrieving company-specific dashboard statistics
    path("employee-dashboard/", EmployeeDashboardStatsView.as_view(), name="employee-dashboard-stats") # Endpoint for retrieving employee-specific dashboard statistics
]
