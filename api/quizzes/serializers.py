import base64
from rest_framework import serializers
from .models import Quiz, Question, Answer

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
    document = serializers.SerializerMethodField()
    document_name = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Quiz
        fields = ["id", "title", "description", "difficulty", "questions", "document", "document_name", "duration"]

    def get_document(self, obj):
        """Konvertuje binarni fajl u base64 string za frontend."""
        if obj.document:
            return base64.b64encode(obj.document).decode('utf-8')
        return None

    def validate_questions(self, value):
        if not value:
            raise serializers.ValidationError("Quiz must contain at least one question.")
        return value

    def create(self, validated_data):
        questions_data = validated_data.pop("questions")
        document_base64 = validated_data.pop("document", None)
        document_name = validated_data.pop("document_name", None)

        # Konvertovanje base64 nazad u binarni format ako je dokument poslat
        if document_base64:
            validated_data["document"] = base64.b64decode(document_base64)
        
        validated_data["document_name"] = document_name
        quiz = Quiz.objects.create(**validated_data)

        for question_data in questions_data:
            answers_data = question_data.pop("answers")
            question = Question.objects.create(quiz=quiz, **question_data)

            for answer_data in answers_data:
                Answer.objects.create(question=question, **answer_data)

        return quiz

    def update(self, instance, validated_data):
        questions_data = validated_data.pop("questions", [])
        document_base64 = validated_data.pop("document", None)
        document_name = validated_data.pop("document_name", None)

        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.difficulty = validated_data.get("difficulty", instance.difficulty)
        instance.duration = validated_data.get("duration", instance.duration)

        # Ako je nov dokument poslat, ažuriraj ga
        if document_base64:
            instance.document = base64.b64decode(document_base64)

        if document_name:
            instance.document_name = document_name

        instance.save()

        instance.questions.all().delete()
        for question_data in questions_data:
            answers_data = question_data.pop("answers", [])
            question = Question.objects.create(quiz=instance, **question_data)

            for answer_data in answers_data:
                Answer.objects.create(question=question, **answer_data)

        return instance
