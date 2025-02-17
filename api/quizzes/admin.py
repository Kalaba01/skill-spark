from django.contrib import admin
from .models import Quiz, Question, Answer, PassedQuizzes

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "difficulty", "created_at")
    search_fields = ("title", "company__company_name")
    list_filter = ("difficulty", "company")
    inlines = [QuestionInline]

class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "quiz")
    search_fields = ("text", "quiz__title")
    inlines = [AnswerInline]

class AnswerAdmin(admin.ModelAdmin):
    list_display = ("text", "question", "is_correct")
    list_filter = ("is_correct",)

class PassedQuizzesAdmin(admin.ModelAdmin):
    list_display = ("employee", "quiz")
    search_fields = ("employee__first_name", "employee__last_name", "quiz__title")
    list_filter = ("quiz", "employee")

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(PassedQuizzes, PassedQuizzesAdmin)
