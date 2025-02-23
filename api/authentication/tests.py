from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core import mail
from .models import Company
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

# Tests for the User model
class UserModelTest(TestCase):
    def test_create_user(self):
        """Test creating a new user with email, password, and role."""
        user = User.objects.create_user(
            email="test@example.com",
            password="TestPass123",
            role=User.COMPANY
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("TestPass123"))
        self.assertEqual(user.role, User.COMPANY)

    def test_create_superuser(self):
        """Test creating a superuser with admin privileges."""
        admin = User.objects.create_superuser(email="admin@example.com", password="AdminPass123")
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)
        self.assertEqual(admin.role, User.ADMIN)


# Tests for the Company model
class CompanyModelTest(TestCase):
    def test_create_company(self):
        """Test creating a company and linking it to a user."""
        user = User.objects.create_user(
            email="company@example.com",
            password="TestPass123",
            role=User.COMPANY
        )
        company = Company.objects.create(user=user, company_name="Test Company")

        self.assertEqual(company.user.email, "company@example.com")
        self.assertEqual(company.company_name, "Test Company")


# Tests for Company registration API
class RegisterCompanyAPITest(TestCase):
    def setUp(self):
        """Set up API client and registration URL before each test."""
        self.client = APIClient()
        self.register_url = "/api/auth/register/"

    def test_register_company_success_and_sends_email(self):
        """Test successful company registration and email confirmation."""
        data = {
            "email": "newcompany@example.com",
            "password": "StrongPass123",
            "company_name": "New Company"
        }

        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)

        # Check if an email is sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Welcome to SkillSpark", mail.outbox[0].subject)

        # Check email content
        html_body = mail.outbox[0].alternatives[0][0]
        self.assertIn("New Company", html_body)
        self.assertIn("http://localhost:3000/", html_body)

    def test_register_company_missing_field(self):
        """Test registration failure when required fields are missing."""
        data = {
            "email": "newcompany@example.com",
            "password": "StrongPass123"
        }

        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("company_name", response.data)

        # No email should be sent
        self.assertEqual(len(mail.outbox), 0)

    def test_register_company_duplicate_email(self):
        """Test registration failure when using an already registered email."""
        User.objects.create_user(email="existing@example.com", password="TestPass123", role=User.COMPANY)

        data = {
            "email": "existing@example.com",
            "password": "StrongPass123",
            "company_name": "Duplicate Company"
        }

        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # No email should be sent
        self.assertEqual(len(mail.outbox), 0)

# Tests for User Login API
class LoginAPITest(TestCase):
    def setUp(self):
        """Set up API client, login URL, and a test user before each test."""
        self.client = APIClient()
        self.login_url = "/api/auth/login/"
        
        self.user = User.objects.create_user(
            email="user@example.com",
            password="TestPass123",
            role=User.COMPANY
        )

    def test_login_success(self):
        """Test successful login with correct credentials."""
        data = {
            "email": "user@example.com",
            "password": "TestPass123"
        }

        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["user"]["email"], "user@example.com")
        self.assertEqual(response.data["user"]["role"], self.user.role)

    def test_login_invalid_password(self):
        """Test login failure with incorrect password."""
        data = {
            "email": "user@example.com",
            "password": "WrongPass123"
        }

        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_login_nonexistent_user(self):
        """Test login failure for a non-existent user."""
        data = {
            "email": "fakeuser@example.com",
            "password": "FakePass123"
        }

        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
