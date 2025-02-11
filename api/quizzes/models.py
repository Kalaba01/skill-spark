from django.db import models
from authentication.models import Company

class Quiz(models.Model):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

    DIFFICULTY_CHOICES = [
        (EASY, "easy"),
        (MEDIUM, "medium"),
        (HARD, "hard")
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default=EASY)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="quizzes")
    created_at = models.DateTimeField(auto_now_add=True)

    document = models.BinaryField(blank=True, null=True)
    document_name = models.CharField(max_length=255, blank=True, null=True)
    duration = models.PositiveIntegerField(default=30)

    def __str__(self):
        return f"{self.title} ({self.company.company_name})"

class Question(models.Model):
    text = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")

    def __str__(self):
        return f"Question: {self.text}"

class Answer(models.Model):
    text = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer: {self.text} (Tačan: {self.is_correct})"
