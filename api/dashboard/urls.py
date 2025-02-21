from django.urls import path
from .views import AdminDashboardStatsView, CompanyDashboardStatsView, EmployeeDashboardStatsView

urlpatterns = [
    path("admin-dashboard/", AdminDashboardStatsView.as_view(), name="admin-dashboard-stats"),
    path("company-dashboard/", CompanyDashboardStatsView.as_view(), name="company-dashboard-stats"),
    path("employee-dashboard/", EmployeeDashboardStatsView.as_view(), name="employee-dashboard-stats")
]
