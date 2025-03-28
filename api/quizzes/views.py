from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from authentication.models import User
from .models import Quiz, Question, Answer, PassedQuizzes
from .serializers import (
    QuizSerializer,
    QuizDetailSerializer,
    QuizTakeSerializer,
    PassedQuizSerializer,
    AdminQuizSerializer
)


class QuizListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating quizzes.
    - Only authenticated users can access.
    - Company users can create quizzes for their employees.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuizSerializer

    def get_queryset(self):
        return Quiz.objects.filter(company=self.request.user.company_profile)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company_profile)


class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a quiz.
    - Only company users can modify their own quizzes.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()

    def get_queryset(self):
        return Quiz.objects.filter(company=self.request.user.company_profile)


class EmployeeQuizListView(generics.ListAPIView):
    """
    API view for employees to list quizzes they haven't taken yet.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuizSerializer

    def get_queryset(self):
        employee = self.request.user.employee_profile
        passed_quizzes = PassedQuizzes.objects.filter(employee=employee).values_list(
            "quiz_id", flat=True
        )

        return Quiz.objects.filter(company=employee.company).exclude(
            id__in=passed_quizzes
        )


class QuizDetailPublicView(generics.RetrieveAPIView):
    """
    API view for retrieving quiz details while ensuring access permissions.
    - Employees can only access quizzes from their own company.
    - Companies can only access their own quizzes.
    """

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
    """
    API view for employees to take a quiz.
    - Validates answers and records the result.
    - Sends an email with quiz results.
    """

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
        """
        Handles quiz submission.

        - Compares submitted answers with correct answers.
        - Determines pass/fail status.
        - Sends an email with the results.
        """
        quiz = self.get_object()
        data = request.data
        employee = request.user.employee_profile

        correct_answers = 0
        total_questions = quiz.questions.count()

        for question in quiz.questions.all():
            selected_answers = data.get(str(question.id), [])

            valid_answer_ids = set(question.answers.values_list("id", flat=True))
            if not set(selected_answers).issubset(valid_answer_ids):
                raise ValidationError({"error": "Invalid answer selected."})

            correct_choices = list(
                question.answers.filter(is_correct=True).values_list("id", flat=True)
            )

            if set(selected_answers) == set(correct_choices):
                correct_answers += 1

        passing_threshold = int((70 / 100) * total_questions)
        passed = correct_answers >= passing_threshold

        subject = "Quiz Results - " + quiz.title
        context = {
            "employee_name": f"{employee.first_name} {employee.last_name}",
            "quiz_title": quiz.title,
            "correct_answers": correct_answers,
            "total_questions": total_questions,
            "passed": passed,
        }

        if passed:
            PassedQuizzes.objects.get_or_create(
                employee=request.user.employee_profile, quiz=quiz
            )

        email_html = render_to_string(
            f"quiz_{"passed" if passed else "failed"}.html", context
        )
        email_text = strip_tags(email_html)

        send_mail(
            subject,
            email_text,
            settings.DEFAULT_FROM_EMAIL,
            [employee.user.email],
            html_message=email_html,
        )

        return Response(
            {
                "correct_answers": correct_answers,
                "total_questions": total_questions,
                "passed": passed,
            },
            status=status.HTTP_200_OK,
        )


class EmployeePassedQuizzesView(generics.ListAPIView):
    """
    API view for retrieving a list of quizzes an employee has passed.
    - Only authenticated users can access.
    - Employees can only see quizzes they have completed.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PassedQuizSerializer

    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, "employee_profile"):
            raise PermissionDenied(
                "You do not have permission to access this resource."
            )

        employee = self.request.user.employee_profile
        passed_quizzes = PassedQuizzes.objects.filter(employee=employee).values_list(
            "quiz_id", flat=True
        )

        return (
            PassedQuizzes.objects.filter(employee=employee)
            .select_related("quiz")
            .order_by("-passed_date")
        )


class AdminQuizListView(generics.ListAPIView):
    """
    API view for admins to list all quizzes from all companies.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AdminQuizSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role != User.ADMIN:
            raise PermissionDenied(
                "You do not have permission to access this resource."
            )
        return Quiz.objects.all()
