from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from authentication.models import User
from .models import Quiz, Question, Answer
from .serializers import QuizSerializer, QuizDetailSerializer, QuizTakeSerializer

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

class QuizTakeView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuizTakeSerializer

    def get_object(self):
        user = self.request.user
        quiz_id = self.kwargs["pk"]

        try:
            quiz = Quiz.objects.get(pk=quiz_id)
        except Quiz.DoesNotExist:
            raise NotFound("Quiz not found.")

        if user.role == User.EMPLOYEE and quiz.company != user.employee_profile.company:
            raise PermissionDenied("You do not have permission to take this quiz.")

        return quiz

    def get(self, request, *args, **kwargs):
        quiz = self.get_object()
        serializer = self.get_serializer(quiz)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        quiz = self.get_object()
        data = request.data

        correct_answers = 0
        total_questions = quiz.questions.count()

        for question in quiz.questions.all():
            selected_answers = data.get(str(question.id), [])

            valid_answer_ids = set(question.answers.values_list("id", flat=True))
            if not set(selected_answers).issubset(valid_answer_ids):
                raise ValidationError({"error": "Invalid answer selected."})

            correct_choices = list(question.answers.filter(is_correct=True).values_list("id", flat=True))

            if set(selected_answers) == set(correct_choices):
                correct_answers += 1

        return Response({"correct_answers": correct_answers, "total_questions": total_questions}, status=status.HTTP_200_OK)
