from rest_framework import serializers
from .models import Quiz, Question, Answer, PassedQuizzes

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "text", "is_correct"]

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "text", "answers"]

    def create(self, validated_data):
        answers_data = validated_data.pop("answers")
        question = Question.objects.create(**validated_data)
        
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)

        return question

    def update(self, instance, validated_data):
        answers_data = validated_data.pop("answers", [])

        instance.text = validated_data.get("text", instance.text)
        instance.save()

        instance.answers.all().delete()
        for answer_data in answers_data:
            Answer.objects.create(question=instance, **answer_data)

        return instance

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ["id", "title", "description", "difficulty", "questions", "duration"]

    def validate_questions(self, value):
        if not value:
            raise serializers.ValidationError("Quiz must contain at least one question.")
        return value

    def create(self, validated_data):
        questions_data = validated_data.pop("questions")
        quiz = Quiz.objects.create(**validated_data)

        for question_data in questions_data:
            answers_data = question_data.pop("answers")
            question = Question.objects.create(quiz=quiz, **question_data)

            for answer_data in answers_data:
                Answer.objects.create(question=question, **answer_data)

        return quiz

    def update(self, instance, validated_data):
        questions_data = validated_data.pop("questions", [])

        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.difficulty = validated_data.get("difficulty", instance.difficulty)
        instance.duration = validated_data.get("duration", instance.duration)
        instance.save()

        instance.questions.all().delete()
        for question_data in questions_data:
            answers_data = question_data.pop("answers", [])
            question = Question.objects.create(quiz=instance, **question_data)

            for answer_data in answers_data:
                Answer.objects.create(question=question, **answer_data)

        return instance

class QuizDetailSerializer(serializers.ModelSerializer):
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ["id", "title", "description", "difficulty", "duration", "question_count"]

    def get_question_count(self, obj):
        return obj.questions.count()

class QuizTakeSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ["id", "title", "duration", "questions"]

    def get_questions(self, obj):
        return [
            {
                "id": question.id,
                "text": question.text,
                "answers": [{"id": answer.id, "text": answer.text} for answer in question.answers.all()]
            }
            for question in obj.questions.all()
        ]

class PassedQuizSerializer(serializers.ModelSerializer):
    passed_date = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = PassedQuizzes
        fields = ["id", "quiz", "passed_date"]
        depth = 1
