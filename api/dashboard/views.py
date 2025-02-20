from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from authentication.models import User
from quizzes.models import Quiz

class AdminDashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != User.ADMIN:
            return Response({"error": "Unauthorized"}, status=403)

        stats = {
            "admins": User.objects.filter(role=User.ADMIN).count(),
            "companies": User.objects.filter(role=User.COMPANY).count(),
            "employees": User.objects.filter(role=User.EMPLOYEE).count(),
            "quizzes": Quiz.objects.count(),
        }
        
        return Response(stats)
