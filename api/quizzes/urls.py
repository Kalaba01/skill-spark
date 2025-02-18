from django.urls import path
from .views import (
    QuizListCreateView,
    QuizDetailView,
    EmployeeQuizListView,
    EmployeePassedQuizzesView,
    QuizDetailPublicView,
    QuizTakeView
)

urlpatterns = [
    path("", QuizListCreateView.as_view(), name="quiz-list-create"),
    path("<int:pk>/", QuizDetailView.as_view(), name="quiz-detail"),
    path("employee-quizzes/", EmployeeQuizListView.as_view(), name="employee-quiz-list"),
    path("employee-passed-quizzes/", EmployeePassedQuizzesView.as_view(), name="employee-passed-quizzes"),
    path("<int:pk>/detail/", QuizDetailPublicView.as_view(), name="quiz-detail-public"),
    path("<int:pk>/take/", QuizTakeView.as_view(), name="quiz-take")
]
