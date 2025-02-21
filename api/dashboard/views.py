from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from authentication.models import User, Company, Employee
from quizzes.models import Quiz, PassedQuizzes

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

class EmployeeDashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != User.EMPLOYEE:
            raise PermissionDenied("Unauthorized access")

        employee = request.user.employee_profile
        passed_quizzes = PassedQuizzes.objects.filter(employee=employee).order_by("-passed_date")

        last_quiz = passed_quizzes.first()
        last_quiz_data = {
            "title": last_quiz.quiz.title if last_quiz else None,
            "date": last_quiz.passed_date.strftime("%Y-%m-%d") if last_quiz else None
        }

        all_quizzes = Quiz.objects.filter(company=employee.company)
        passed_quiz_ids = passed_quizzes.values_list("quiz_id", flat=True)
        recommended_quiz = all_quizzes.exclude(id__in=passed_quiz_ids).first()

        recommended_quiz_data = {
            "title": recommended_quiz.title if recommended_quiz else None
        }

        stats = {
            "passed_quizzes": passed_quizzes.count(),
            "last_quiz": last_quiz_data,
            "recommended_quiz": recommended_quiz_data
        }

        return Response(stats)
