from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Quiz, Question, Answer, Company
from authentication.models import Employee

User = get_user_model()


class QuizAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.company_user = User.objects.create_user(
            email="company@example.com",
            password="TestPass123",
            role=User.COMPANY
        )
        self.company = Company.objects.create(user=self.company_user, company_name="Test Company")

        self.employee_user = User.objects.create_user(
            email="employee@example.com",
            password="TestPass123",
            role=User.EMPLOYEE
        )

        self.employee = Employee.objects.create(
            user=self.employee_user,
            first_name="John",
            last_name="Doe",
            company=self.company
        )

        self.client.force_authenticate(user=self.company_user)

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
        self.question1 = Question.objects.create(quiz=self.quiz, text="What is 2 + 2?")
        self.answer1 = Answer.objects.create(question=self.question1, text="3", is_correct=False)
        self.answer2 = Answer.objects.create(question=self.question1, text="4", is_correct=True)
        self.answer3 = Answer.objects.create(question=self.question1, text="5", is_correct=False)

        self.question2 = Question.objects.create(quiz=self.quiz, text="Which are primary colors?")
        self.answer4 = Answer.objects.create(question=self.question2, text="Red", is_correct=True)
        self.answer5 = Answer.objects.create(question=self.question2, text="Blue", is_correct=True)
        self.answer6 = Answer.objects.create(question=self.question2, text="Green", is_correct=False)

        self.quiz_url = "/api/quizzes/"
        self.quiz_detail_url = f"/api/quizzes/{self.quiz.id}/"
        self.quiz_take_url = f"/api/quizzes/{self.quiz.id}/take/"

        self.employee_quizzes_url = "/api/quizzes/employee-quizzes/"
        self.employee_quiz_detail_url = f"/api/quizzes/{self.quiz.id}/detail/"

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

    def test_employee_can_get_company_quizzes(self):
        self.client.force_authenticate(user=self.employee_user)
        response = self.client.get(self.employee_quizzes_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], self.quiz.title)
        self.assertEqual(response.data[0]["duration"], self.quiz.duration)

    def test_employee_can_get_quiz_detail(self):
        self.client.force_authenticate(user=self.employee_user)
        response = self.client.get(self.employee_quiz_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.quiz.title)
        self.assertEqual(response.data["description"], self.quiz.description)
        self.assertEqual(response.data["difficulty"], self.quiz.difficulty)
        self.assertEqual(response.data["duration"], self.quiz.duration)
        self.assertEqual(response.data["question_count"], 2)

    def test_employee_cannot_access_other_company_quizzes(self):
        other_company_user = User.objects.create_user(
            email="othercompany@example.com",
            password="TestPass123",
            role=User.COMPANY
        )
        other_company = Company.objects.create(user=other_company_user, company_name="Other Company")

        other_employee_user = User.objects.create_user(
            email="otheremployee@example.com",
            password="TestPass123",
            role=User.EMPLOYEE
        )
        other_employee = Employee.objects.create(
            user=other_employee_user,
            first_name="Jane",
            last_name="Smith",
            company=other_company
        )

        other_quiz = Quiz.objects.create(
            title="Other Company Quiz",
            description="A quiz from another company",
            difficulty="hard",
            duration=45,
            company=other_company
        )

        self.client.force_authenticate(user=other_employee_user)
        response = self.client.get(self.employee_quiz_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_unauthorized_user_cannot_access_quiz_detail(self):
        self.client.logout()
        response = self.client.get(self.employee_quiz_detail_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_employee_can_get_quiz_for_taking(self):
        self.client.force_authenticate(user=self.employee_user)
        response = self.client.get(self.quiz_take_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.quiz.id)
        self.assertEqual(response.data["title"], self.quiz.title)
        self.assertEqual(len(response.data["questions"]), 2)

    def test_employee_cannot_access_other_company_quiz_for_taking(self):
        other_company_user = User.objects.create_user(
            email="othercompany@example.com",
            password="TestPass123",
            role=User.COMPANY
        )
        other_company = Company.objects.create(user=other_company_user, company_name="Other Company")

        other_employee_user = User.objects.create_user(
            email="otheremployee@example.com",
            password="TestPass123",
            role=User.EMPLOYEE
        )
        Employee.objects.create(
            user=other_employee_user,
            first_name="Jane",
            last_name="Smith",
            company=other_company
        )

        self.client.force_authenticate(user=other_employee_user)
        response = self.client.get(self.quiz_take_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_can_submit_quiz_answers(self):
        self.client.force_authenticate(user=self.employee_user)

        quiz_answers = {
            str(self.question1.id): [self.answer2.id],
            str(self.question2.id): [self.answer4.id, self.answer5.id]
        }

        response = self.client.post(self.quiz_take_url, quiz_answers, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["correct_answers"], 2)
        self.assertEqual(response.data["total_questions"], 2)

    def test_employee_receives_correct_count_when_some_answers_are_wrong(self):
        self.client.force_authenticate(user=self.employee_user)

        quiz_answers = {
            str(self.question1.id): [self.answer1.id],
            str(self.question2.id): [self.answer4.id]
        }

        response = self.client.post(self.quiz_take_url, quiz_answers, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["correct_answers"], 0)
        self.assertEqual(response.data["total_questions"], 2)

    def test_employee_cannot_submit_invalid_quiz_answers(self):
        self.client.force_authenticate(user=self.employee_user)

        invalid_quiz_answers = {
            str(self.question1.id): ["9999"],
            "9999": [self.answer2.id]
        }

        response = self.client.post(self.quiz_take_url, invalid_quiz_answers, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_user_cannot_take_quiz(self):
        self.client.logout()
        response = self.client.get(self.quiz_take_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_user_cannot_submit_quiz_answers(self):
        self.client.logout()
        quiz_answers = {
            str(self.question1.id): [self.answer2.id],
            str(self.question2.id): [self.answer4.id, self.answer5.id]
        }

        response = self.client.post(self.quiz_take_url, quiz_answers, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
