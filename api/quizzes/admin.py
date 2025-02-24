from django.contrib import admin
from .models import Quiz, Question, Answer, PassedQuizzes

# Inline admin class for Answer to be displayed within the Question admin panel
class AnswerInline(admin.TabularInline):
    """
    Inline display for answers within the question admin panel.
    Allows adding multiple answers directly inside a question entry.
    """
    model = Answer
    extra = 1 # Provides an empty field for adding new answers

# Inline admin class for Question to be displayed within the Quiz admin panel
class QuestionInline(admin.TabularInline):
    """
    Inline display for questions within the quiz admin panel.
    Allows adding multiple questions directly inside a quiz entry.
    """
    model = Question
    extra = 1 # Provides an empty field for adding new questions

# Custom admin panel for managing quizzes
class QuizAdmin(admin.ModelAdmin):
    """
    Custom admin panel configuration for Quiz model.
    Provides search, filtering, and inline question management.
    """
    list_display = ("title", "company", "difficulty", "created_at")
    search_fields = ("title", "company__company_name")
    list_filter = ("difficulty", "company")
    inlines = [QuestionInline]

# Custom admin panel for managing questions
class QuestionAdmin(admin.ModelAdmin):
    """
    Custom admin panel configuration for Question model.
    Provides search, filtering, and inline answer management.
    """
    list_display = ("text", "quiz")
    search_fields = ("text", "quiz__title")
    inlines = [AnswerInline]

# Custom admin panel for managing answers
class AnswerAdmin(admin.ModelAdmin):
    """
    Custom admin panel configuration for Answer model.
    Provides filtering options for correct/incorrect answers.
    """
    list_display = ("text", "question", "is_correct")
    list_filter = ("is_correct",)

# Custom admin panel for tracking passed quizzes
class PassedQuizzesAdmin(admin.ModelAdmin):
    """
    Custom admin panel configuration for PassedQuizzes model.
    Provides search and filtering options for tracking quiz completion.
    """
    list_display = ("employee", "quiz")
    search_fields = ("employee__first_name", "employee__last_name", "quiz__title")
    list_filter = ("quiz", "employee")

# Registering models with their respective admin configurations
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(PassedQuizzes, PassedQuizzesAdmin)
