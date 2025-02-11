from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Quiz, Question, Answer, Company

User = get_user_model()


class QuizAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="company@example.com",
            password="TestPass123",
            role=User.COMPANY
        )
        self.company = Company.objects.create(user=self.user, company_name="Test Company")
        self.client.force_authenticate(user=self.user)

        self.quiz_data = {
            "title": "Sample Quiz",
            "description": "A test quiz description.",
            "difficulty": "easy",
            "duration": 30,
            "questions": [
                {
                    "text": "What is 2 + 2?",
                    "answers": [
                        {"text": "3", "is_correct": False},
                        {"text": "4", "is_correct": True},
                        {"text": "5", "is_correct": False}
                    ]
                }
            ]
        }

        self.quiz = Quiz.objects.create(
            title="Existing Quiz",
            description="An existing quiz",
            difficulty="medium",
            duration=25,
            company=self.company
        )
        self.question = Question.objects.create(quiz=self.quiz, text="What is the capital of France?")
        self.answer1 = Answer.objects.create(question=self.question, text="Paris", is_correct=True)
        self.answer2 = Answer.objects.create(question=self.question, text="London", is_correct=False)

        self.quiz_url = "/api/quizzes/"
        self.quiz_detail_url = f"/api/quizzes/{self.quiz.id}/"

    def test_create_quiz(self):
        response = self.client.post(self.quiz_url, self.quiz_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quiz.objects.count(), 2)
        self.assertEqual(response.data["title"], self.quiz_data["title"])
        self.assertEqual(response.data["duration"], self.quiz_data["duration"])

    def test_get_quizzes(self):
        response = self.client.get(self.quiz_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["duration"], self.quiz.duration)

    def test_get_single_quiz(self):
        response = self.client.get(self.quiz_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.quiz.title)
        self.assertEqual(response.data["duration"], self.quiz.duration)

    def test_update_quiz(self):
        updated_data = {
            "title": "Updated Quiz",
            "description": "Updated description",
            "difficulty": "hard",
            "duration": 45,
            "questions": [
                {
                    "text": "What is the square root of 16?",
                    "answers": [
                        {"text": "2", "is_correct": False},
                        {"text": "4", "is_correct": True},
                        {"text": "6", "is_correct": False}
                    ]
                }
            ]
        }
        response = self.client.put(self.quiz_detail_url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.quiz.refresh_from_db()
        self.assertEqual(self.quiz.title, "Updated Quiz")
        self.assertEqual(self.quiz.difficulty, "hard")
        self.assertEqual(self.quiz.duration, 45)

    def test_delete_quiz(self):
        response = self.client.delete(self.quiz_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Quiz.objects.count(), 0)

    def test_create_quiz_without_questions(self):
        data = {
            "title": "Quiz Without Questions",
            "description": "No questions here",
            "difficulty": "medium",
            "duration": 20,
            "questions": []
        }
        response = self.client.post(self.quiz_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_access(self):
        self.client.logout()
        response = self.client.get(self.quiz_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
