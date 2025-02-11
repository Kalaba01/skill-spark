from django.urls import path
from .views import QuizListCreateView, QuizDetailView, EmployeeQuizListView

urlpatterns = [
    path("", QuizListCreateView.as_view(), name="quiz-list-create"),
    path("<int:pk>/", QuizDetailView.as_view(), name="quiz-detail"),
    path("employee-quizzes/", EmployeeQuizListView.as_view(), name="employee-quiz-list")
]
