from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from authentication.models import User, Company, Employee
from quizzes.models import Quiz, PassedQuizzes

class AdminDashboardStatsView(APIView):
    """
    API view for retrieving statistics for the admin dashboard.
    Only accessible to users with the ADMIN role.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieves platform-wide statistics.

        - Ensures the user has the ADMIN role.
        - Returns a JSON response containing:
          - Total number of admins
          - Total number of companies
          - Total number of employees
          - Total number of quizzes
        """
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
    """
    API view for retrieving statistics for a company's dashboard.
    Only accessible to users with the COMPANY role.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieves statistics for the authenticated company.

        - Ensures the user has the COMPANY role.
        - Returns a JSON response containing:
          - Total number of employees in the company
          - Total number of quizzes created by the company
        """
        if request.user.role != User.COMPANY:
            raise PermissionDenied("Unauthorized access")

        company = request.user.company_profile

        stats = {
            "employees": Employee.objects.filter(company=company).count(),
            "quizzes": Quiz.objects.filter(company=company).count(),
        }

        return Response(stats)

class EmployeeDashboardStatsView(APIView):
    """
    API view for retrieving statistics for an employee's dashboard.
    Only accessible to users with the EMPLOYEE role.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieves statistics for the authenticated employee.

        - Ensures the user has the EMPLOYEE role.
        - Returns a JSON response containing:
          - Total number of quizzes taken (passed_quizzes)
          - Total number of quizzes in the company
          - Details of the last quiz taken (title, date)
          - Recommended quiz for the employee
        """
        if request.user.role != User.EMPLOYEE:
            raise PermissionDenied("Unauthorized access")

        employee = request.user.employee_profile
        passed_quizzes = PassedQuizzes.objects.filter(employee=employee).order_by("-passed_date")

        # Get the last quiz taken
        last_quiz = passed_quizzes.first()
        last_quiz_data = {
            "title": last_quiz.quiz.title if last_quiz else None,
            "date": last_quiz.passed_date.strftime("%Y-%m-%d") if last_quiz else None
        }

        # Get all quizzes from the employee's company
        all_quizzes = Quiz.objects.filter(company=employee.company)
        total_quizzes = all_quizzes.count()

        # Get a recommended quiz (a first quiz the employee has not taken yet)
        passed_quiz_ids = passed_quizzes.values_list("quiz_id", flat=True)
        recommended_quiz = all_quizzes.exclude(id__in=passed_quiz_ids).first()

        recommended_quiz_data = {
            "title": recommended_quiz.title if recommended_quiz else None,
            "description": recommended_quiz.description if recommended_quiz else None
        }

        stats = {
            "passed_quizzes": passed_quizzes.count(),
            "total_quizzes": total_quizzes,
            "last_quiz": last_quiz_data,
            "recommended_quiz": recommended_quiz_data
        }

        return Response(stats)
