from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from authentication.models import User, Company, Employee
from quizzes.models import Quiz

class AdminDashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != User.ADMIN:
            raise PermissionDenied("Unauthorized access")

        stats = {
            "admins": User.objects.filter(role=User.ADMIN).count(),
            "companies": User.objects.filter(role=User.COMPANY).count(),
            "employees": User.objects.filter(role=User.EMPLOYEE).count(),
            "quizzes": Quiz.objects.count(),
        }

        return Response(stats)

class CompanyDashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != User.COMPANY:
            raise PermissionDenied("Unauthorized access")

        company = request.user.company_profile

        stats = {
            "employees": Employee.objects.filter(company=company).count(),
            "quizzes": Quiz.objects.filter(company=company).count(),
        }

        return Response(stats)
