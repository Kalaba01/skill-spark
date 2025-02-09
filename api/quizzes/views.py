from rest_framework import generics, permissions
from .models import Quiz
from .serializers import QuizSerializer

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
