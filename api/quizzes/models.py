from django.db import models
from authentication.models import Company, Employee

# Quiz model represents a quiz created by a company for employees
class Quiz(models.Model):
    """
    Represents a quiz that companies create for employees.
    Contains a title, description, difficulty level, duration, and a reference to the company that owns it.
    """

    # Difficulty level choices
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
    duration = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.company.company_name})"

# Question model represents a single question that belongs to a quiz
class Question(models.Model):
    """
    Represents a question in a quiz.
    A quiz can have multiple questions.
    """


    text = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")

    def __str__(self):
        return f"Question: {self.text}"

# Answer model represents a possible answer for a question
class Answer(models.Model):
    """
    Represents an answer option for a specific question.
    Each question can have multiple answers, but at least one should be correct.
    """

    text = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer: {self.text} (Tačan: {self.is_correct})"

# PassedQuizzes model stores records of employees who have successfully completed quizzes
class PassedQuizzes(models.Model):
    """
    Tracks quizzes that employees have passed.
    Stores a reference to the employee, the quiz they passed, and the date of completion.
    """
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="passed_quizzes")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="passed_by_employees")
    passed_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("employee", "quiz")

    def __str__(self):
        return f"{self.employee.user.email} - {self.quiz.title} ({self.passed_date.strftime('%Y-%m-%d')})"
