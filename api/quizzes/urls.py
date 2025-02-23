from django.urls import path
from .views import (
    QuizListCreateView,
    QuizDetailView,
    EmployeeQuizListView,
    EmployeePassedQuizzesView,
    QuizDetailPublicView,
    QuizTakeView,
    AdminQuizListView
)

urlpatterns = [
    path("", QuizListCreateView.as_view(), name="quiz-list-create"), # Endpoint for creating a quiz or listing all quizzes
    path("<int:pk>/", QuizDetailView.as_view(), name="quiz-detail"), # Endpoint for retrieving, updating, or deleting a specific quiz
    path("employee-quizzes/", EmployeeQuizListView.as_view(), name="employee-quiz-list"), # Endpoint for employees to see available quizzes they haven't taken yet
    path("employee-passed-quizzes/", EmployeePassedQuizzesView.as_view(), name="employee-passed-quizzes"), # Endpoint for employees to view quizzes they have passed
    path("<int:pk>/detail/", QuizDetailPublicView.as_view(), name="quiz-detail-public"), # Public quiz detail view
    path("<int:pk>/take/", QuizTakeView.as_view(), name="quiz-take"), # Endpoint for employees to take a quiz
    path("admin/all-quizzes/", AdminQuizListView.as_view(), name="admin-all-quizzes") # Endpoint for admin users to see all quizzes from all companies
]
