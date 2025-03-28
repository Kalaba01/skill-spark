from unittest.mock import patch
from django.core.mail import send_mail
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Quiz, Question, Answer, Company, PassedQuizzes
from authentication.models import Employee

User = get_user_model()


class BaseQuizTestCase(TestCase):
    """Base setup for quiz-related test cases."""
    def setUp(self):
        """Create test users, companies, quizzes, and questions."""
        self.client = APIClient()

        # Create company and employee users
        self.company_user = User.objects.create_user(
            email="company@example.com",
            password="TestPass123",
            role=User.COMPANY
        )
        self.company = Company.objects.create(
            user=self.company_user,
            company_name="Test Company"
        )

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

        # Create a quiz with questions and answers
        self.quiz = Quiz.objects.create(
            title="Existing Quiz",
            description="An existing quiz",
            difficulty="medium",
            duration=25,
            company=self.company
        )
        self.question1 = Question.objects.create(
            quiz=self.quiz,
            text="What is 2 + 2?"
        )
        self.answer1 = Answer.objects.create(
            question=self.question1,
            text="3",
            is_correct=False
        )
        self.answer2 = Answer.objects.create(
            question=self.question1,
            text="4",
            is_correct=True
        )
        self.answer3 = Answer.objects.create(
            question=self.question1,
            text="5",
            is_correct=False
        )

        self.question2 = Question.objects.create(
            quiz=self.quiz,
            text="Which are primary colors?"
        )
        self.answer4 = Answer.objects.create(
            question=self.question2,
            text="Red",
            is_correct=True
        )
        self.answer5 = Answer.objects.create(
            question=self.question2,
            text="Blue",
            is_correct=True
        )
        self.answer6 = Answer.objects.create(
            question=self.question2,
            text="Green",
            is_correct=False
        )

        # Sample quiz data for POST requests
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

        # Define API endpoints
        self.quiz_url = "/api/quizzes/"
        self.quiz_detail_url = f"/api/quizzes/{self.quiz.id}/"
        self.quiz_take_url = f"/api/quizzes/{self.quiz.id}/take/"
        self.employee_quizzes_url = "/api/quizzes/employee-quizzes/"
        self.employee_quiz_detail_url = f"/api/quizzes/{self.quiz.id}/detail/"
        self.passed_quizzes_url = "/api/quizzes/employee-passed-quizzes/"


class QuizManagementTests(BaseQuizTestCase):
    """Test cases for managing quizzes as a company."""
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.company_user)

    def test_create_quiz(self):
        """Test that a company can create a quiz."""
        response = self.client.post(self.quiz_url, self.quiz_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quiz.objects.count(), 2)
        self.assertEqual(response.data["title"], self.quiz_data["title"])
        self.assertEqual(response.data["duration"], self.quiz_data["duration"])

    def test_get_quizzes(self):
        """Test retrieving the list of quizzes."""
        response = self.client.get(self.quiz_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["duration"], self.quiz.duration)

    def test_get_single_quiz(self):
        """Test retrieving a single quiz by ID."""
        response = self.client.get(self.quiz_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.quiz.title)
        self.assertEqual(response.data["duration"], self.quiz.duration)

    def test_update_quiz(self):
        """Test updating an existing quiz."""
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
        """Test deleting a quiz."""
        response = self.client.delete(self.quiz_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Quiz.objects.count(), 0)

    def test_create_quiz_without_questions(self):
        """Test that a quiz cannot be created without questions."""
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
        """Test that unauthorized users cannot access quizzes."""
        self.client.logout()
        response = self.client.get(self.quiz_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class EmployeeQuizAccessTests(BaseQuizTestCase):
    """Test cases for employee access to quizzes."""
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.employee_user)

    def test_employee_can_get_company_quizzes(self):
        """Test that an employee can retrieve available quizzes from their company."""
        response = self.client.get(self.employee_quizzes_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], self.quiz.title)

        # If an employee has already passed the quiz, it should not be shown
        PassedQuizzes.objects.create(employee=self.employee, quiz=self.quiz)
        response = self.client.get(self.employee_quizzes_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_employee_can_get_quiz_detail(self):
        """Test that an employee can retrieve details of a specific quiz."""
        response = self.client.get(self.employee_quiz_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.quiz.title)
        self.assertEqual(response.data["description"], self.quiz.description)
        self.assertEqual(response.data["difficulty"], self.quiz.difficulty)
        self.assertEqual(response.data["duration"], self.quiz.duration)
        self.assertEqual(response.data["question_count"], 2)

    def test_employee_cannot_access_other_company_quizzes(self):
        """Test that employees cannot access quizzes from another company."""
        other_company_user = User.objects.create_user(
            email="othercompany@example.com",
            password="TestPass123",
            role=User.COMPANY
        )
        other_company = Company.objects.create(
            user=other_company_user,
            company_name="Other Company"
        )
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
        """Test that unauthorized users cannot access quiz details."""
        self.client.logout()
        response = self.client.get(self.employee_quiz_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class QuizTakingTests(BaseQuizTestCase):
    """Test cases for employees taking quizzes."""

    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.employee_user)

    def test_employee_can_get_quiz_for_taking(self):
        """Test that an employee can retrieve a quiz for taking."""
        response = self.client.get(self.quiz_take_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.quiz.id)
        self.assertEqual(len(response.data["questions"]), 2)

    def test_employee_cannot_access_other_company_quiz_for_taking(self):
        """Test that an employee cannot take a quiz from another company."""
        other_company_user = User.objects.create_user(
            email="othercompany@example.com",
            password="TestPass123",
            role=User.COMPANY
        )
        other_company = Company.objects.create(
            user=other_company_user,
            company_name="Other Company"
        )
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

    @patch("quizzes.views.send_mail")
    def test_employee_can_submit_quiz_answers(self, mock_send_mail):
        """Test that an employee can submit answers and pass the quiz."""
        quiz_answers = {
            str(self.question1.id): [self.answer2.id],
            str(self.question2.id): [self.answer4.id, self.answer5.id]
        }
        response = self.client.post(self.quiz_take_url, quiz_answers, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["correct_answers"], 2)
        self.assertEqual(response.data["total_questions"], 2)
        self.assertTrue(response.data["passed"])
        mock_send_mail.assert_called()

    @patch("quizzes.views.send_mail")
    def test_employee_receives_email_even_when_failing_quiz(self, mock_send_mail):
        """Test that an employee still receives an email when failing a quiz."""
        quiz_answers = {
            str(self.question1.id): [self.answer1.id], # Incorrect answer
            str(self.question2.id): [self.answer4.id] # Partial correct
        }
        response = self.client.post(self.quiz_take_url, quiz_answers, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_questions"], 2)
        self.assertFalse(response.data["passed"])
        mock_send_mail.assert_called()

    def test_employee_receives_correct_count_when_some_answers_are_wrong(self):
        """Test that the correct answer count is calculated properly."""
        quiz_answers = {
            str(self.question1.id): [self.answer1.id], # Incorrect answer
            str(self.question2.id): [self.answer4.id]  # Partial correct
        }
        response = self.client.post(self.quiz_take_url, quiz_answers, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["correct_answers"], 0)
        self.assertEqual(response.data["total_questions"], 2)

    @patch("quizzes.views.send_mail")
    def test_employee_cannot_submit_invalid_quiz_answers(self, mock_send_mail):
        """Test that invalid answers cannot be submitted."""
        invalid_quiz_answers = {
            str(self.question1.id): ["9999"], # Invalid answer ID
            "9999": [self.answer2.id]         # Invalid question ID
        }
        response = self.client.post(self.quiz_take_url, invalid_quiz_answers, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        mock_send_mail.assert_not_called()

    def test_unauthorized_user_cannot_take_quiz(self):
        """Test that an unauthenticated user cannot access the quiz."""
        self.client.logout()
        response = self.client.get(self.quiz_take_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_user_cannot_submit_quiz_answers(self):
        """Test that an unauthenticated user cannot submit answers."""
        self.client.logout()
        quiz_answers = {
            str(self.question1.id): [self.answer2.id],
            str(self.question2.id): [self.answer4.id, self.answer5.id]
        }
        response = self.client.post(self.quiz_take_url, quiz_answers, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PassedQuizzesTests(BaseQuizTestCase):
    """Test cases for retrieving passed quizzes."""

    def setUp(self):
        """Set up test data for passed quizzes."""
        super().setUp()
        self.client.force_authenticate(user=self.employee_user)

        # Create quizzes
        self.quiz1 = Quiz.objects.create(
            title="Python Basics",
            description="A quiz on Python fundamentals.",
            difficulty="easy",
            duration=30,
            company=self.company
        )

        # Mark one quiz as passed for the employee
        self.passed_quiz = PassedQuizzes.objects.create(
            employee=self.employee,
            quiz=self.quiz1
        )
        self.quiz2 = Quiz.objects.create(
            title="Advanced Django",
            description="A deep dive into Django.",
            difficulty="hard",
            duration=40,
            company=self.company
        )

    def test_employee_can_get_passed_quizzes(self):
        """Test that an employee can retrieve their list of passed quizzes."""
        response = self.client.get(self.passed_quizzes_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["quiz"]["title"], "Python Basics")

        expected_date = self.passed_quiz.passed_date.strftime("%Y-%m-%d")
        self.assertEqual(response.data[0]["passed_date"], expected_date)

    def test_employee_only_sees_their_own_passed_quizzes(self):
        """Test that an employee can only see their own passed quizzes."""
        # Create another employee and assign a passed quiz to them
        another_employee_user = User.objects.create_user(
            email="employee2@example.com",
            password="TestPass123",
            role=User.EMPLOYEE
        )
        another_employee = Employee.objects.create(
            user=another_employee_user,
            first_name="Jane",
            last_name="Doe",
            company=self.company
        )
        PassedQuizzes.objects.create(employee=another_employee, quiz=self.quiz2)

        # Ensure that the first employee does not see quizzes passed by others
        self.client.force_authenticate(user=self.employee_user)
        response = self.client.get(self.passed_quizzes_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertNotEqual(response.data[0]["quiz"]["title"], "Advanced Django")

    def test_employee_with_no_passed_quizzes_gets_empty_list(self):
        """Test that an employee with no passed quizzes gets an empty list."""
        new_employee_user = User.objects.create_user(
            email="newemployee@example.com",
            password="TestPass123",
            role=User.EMPLOYEE
        )
        new_employee = Employee.objects.create(
            user=new_employee_user,
            first_name="Alice",
            last_name="Smith",
            company=self.company
        )
        self.client.force_authenticate(user=new_employee_user)
        response = self.client.get(self.passed_quizzes_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_unauthorized_user_cannot_access_passed_quizzes(self):
        """Test that unauthorized users cannot access passed quizzes."""
        self.client.logout()
        response = self.client.get(self.passed_quizzes_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class AdminQuizListTests(TestCase):
    """Test cases for the admin viewing all quizzes."""

    def setUp(self):
        """Set up test data for admin quiz retrieval."""
        self.client = APIClient()

        # Create admin user
        self.admin_user = User.objects.create_user(
            email="admin@test.com",
            password="testpass",
            role=User.ADMIN
        )

        # Create company user and company
        self.company_user = User.objects.create_user(
            email="company@test.com",
            password="testpass",
            role=User.COMPANY
        )
        self.company = Company.objects.create(
            user=self.company_user,
            company_name="Test Company"
        )

         # Create quizzes under the company
        self.quiz1 = Quiz.objects.create(
            title="Python Basics",
            description="A quiz on Python fundamentals.",
            difficulty="easy",
            duration=30,
            company=self.company
        )

        self.quiz2 = Quiz.objects.create(
            title="Advanced Django",
            description="A deep dive into Django framework.",
            difficulty="hard",
            duration=40,
            company=self.company
        )

        self.admin_quiz_list_url = "/api/quizzes/admin/all-quizzes/"

    def test_admin_can_get_all_quizzes(self):
        """Test that an admin can retrieve all quizzes."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.admin_quiz_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], "Python Basics")
        self.assertEqual(response.data[1]["title"], "Advanced Django")

    def test_company_cannot_get_all_quizzes(self):
        """Test that a company user cannot access all quizzes."""
        self.client.force_authenticate(user=self.company_user)
        response = self.client.get(self.admin_quiz_list_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_user_cannot_get_quizzes(self):
        """Test that an unauthenticated user cannot access all quizzes."""
        self.client.logout()
        response = self.client.get(self.admin_quiz_list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
