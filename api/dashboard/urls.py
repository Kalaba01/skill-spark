from django.urls import path
from .views import AdminDashboardStatsView

urlpatterns = [
    path("admin-dashboard/", AdminDashboardStatsView.as_view(), name="admin-dashboard-stats")
]
