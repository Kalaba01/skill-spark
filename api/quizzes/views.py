from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound, PermissionDenied
from authentication.models import User
from .models import Quiz
from .serializers import QuizSerializer, QuizDetailSerializer

class QuizListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuizSerializer

    def get_queryset(self):
        return Quiz.objects.filter(company=self.request.user.company_profile)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company_profile)

class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()

    def get_queryset(self):
        return Quiz.objects.filter(company=self.request.user.company_profile)

class EmployeeQuizListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuizSerializer

    def get_queryset(self):
        return Quiz.objects.filter(company=self.request.user.employee_profile.company)

class QuizDetailPublicView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuizDetailSerializer

    def get_object(self):
        user = self.request.user
        quiz_id = self.kwargs["pk"]

        try:
            quiz = Quiz.objects.get(pk=quiz_id)
        except Quiz.DoesNotExist:
            raise NotFound("Quiz not found.")

        if user.role == User.EMPLOYEE and quiz.company != user.employee_profile.company:
            raise PermissionDenied("You do not have permission to access this quiz.")

        if user.role == User.COMPANY and quiz.company != user.company_profile:
            raise PermissionDenied("You do not have permission to access this quiz.")

        return quiz
