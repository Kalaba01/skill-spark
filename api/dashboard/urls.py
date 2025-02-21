from django.urls import path
from .views import AdminDashboardStatsView, CompanyDashboardStatsView

urlpatterns = [
    path("admin-dashboard/", AdminDashboardStatsView.as_view(), name="admin-dashboard-stats"),
    path("company-dashboard/", CompanyDashboardStatsView.as_view(), name="company-dashboard-stats")
]
