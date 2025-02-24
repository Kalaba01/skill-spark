from rest_framework import serializers
from .models import Quiz, Question, Answer, PassedQuizzes

class AnswerSerializer(serializers.ModelSerializer):
    """Serializer for quiz answers."""
    class Meta:
        model = Answer
        fields = ["id", "text", "is_correct"]

class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for quiz questions, including nested answers."""
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "text", "answers"]

    def create(self, validated_data):
        """
        Handles the creation of a question with multiple answers.
        """
        answers_data = validated_data.pop("answers")
        question = Question.objects.create(**validated_data)
        
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)

        return question

    def update(self, instance, validated_data):
        """
        Handles updating a question along with its answers.
        - Deletes existing answers and replaces them with new ones.
        """
        answers_data = validated_data.pop("answers", [])

        instance.text = validated_data.get("text", instance.text)
        instance.save()

        # Remove old answers before adding new ones
        instance.answers.all().delete()

        for answer_data in answers_data:
            Answer.objects.create(question=instance, **answer_data)

        return instance

class QuizSerializer(serializers.ModelSerializer):
    """Serializer for quizzes, including nested questions and answers."""
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ["id", "title", "description", "difficulty", "questions", "duration"]

    def validate_questions(self, value):
        """
        Ensures that a quiz has at least one question.
        """
        if not value:
            raise serializers.ValidationError("Quiz must contain at least one question.")
        return value

    def create(self, validated_data):
        """
        Handles the creation of a quiz with nested questions and answers.
        """
        questions_data = validated_data.pop("questions")
        quiz = Quiz.objects.create(**validated_data)

        for question_data in questions_data:
            answers_data = question_data.pop("answers")
            question = Question.objects.create(quiz=quiz, **question_data)

            for answer_data in answers_data:
                Answer.objects.create(question=question, **answer_data)

        return quiz

    def update(self, instance, validated_data):
        """
        Handles updating a quiz.
        - Updates quiz details and replaces all questions with new ones.
        """
        questions_data = validated_data.pop("questions", [])

        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.difficulty = validated_data.get("difficulty", instance.difficulty)
        instance.duration = validated_data.get("duration", instance.duration)
        instance.save()

        # Remove old questions before adding new ones
        instance.questions.all().delete()

        for question_data in questions_data:
            answers_data = question_data.pop("answers", [])
            question = Question.objects.create(quiz=instance, **question_data)

            for answer_data in answers_data:
                Answer.objects.create(question=question, **answer_data)

        return instance

class QuizDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving quiz details.
    - Includes basic quiz information.
    - Adds a computed field `question_count` to display the number of questions in the quiz.
    """

    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ["id", "title", "description", "difficulty", "duration", "question_count"]

    def get_question_count(self, obj):
        """
        Returns the number of questions in the quiz.
        """
        return obj.questions.count()

class QuizTakeSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving quiz questions when an employee takes a quiz.
    - Includes the quiz title and duration.
    - Fetches all questions and their possible answers.
    """
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ["id", "title", "duration", "questions"]

    def get_questions(self, obj):
        """
        Returns a structured list of questions and possible answers.
        - Only provides answer text, not whether it is correct.
        """
        
        return [
            {
                "id": question.id,
                "text": question.text,
                "answers": [{"id": answer.id, "text": answer.text} for answer in question.answers.all()]
            }
            for question in obj.questions.all()
        ]

class PassedQuizSerializer(serializers.ModelSerializer):
    """Serializer for tracking passed quizzes."""
    passed_date = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = PassedQuizzes
        fields = ["id", "quiz", "passed_date"]
        depth = 1

class AdminQuizSerializer(serializers.ModelSerializer):
    """Serializer for quizzes in the admin panel, including company details."""
    company_name = serializers.CharField(source="company.company_name", read_only=True)

    class Meta:
        model = Quiz
        fields = ["id", "title", "description", "difficulty", "duration", "company_name"]
