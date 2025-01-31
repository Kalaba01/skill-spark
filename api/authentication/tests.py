from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Company
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email="test@example.com",
            password="TestPass123",
            role=User.COMPANY
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("TestPass123"))
        self.assertEqual(user.role, User.COMPANY)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(email="admin@example.com", password="AdminPass123")
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)
        self.assertEqual(admin.role, User.ADMIN)


class CompanyModelTest(TestCase):
    def test_create_company(self):
        user = User.objects.create_user(
            email="company@example.com",
            password="TestPass123",
            role=User.COMPANY
        )
        company = Company.objects.create(user=user, company_name="Test Company")

        self.assertEqual(company.user.email, "company@example.com")
        self.assertEqual(company.company_name, "Test Company")


class RegisterCompanyAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = "/api/auth/register/"

    def test_register_company_success(self):
        data = {
            "email": "newcompany@example.com",
            "password": "StrongPass123",
            "company_name": "New Company"
        }

        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)

    def test_register_company_missing_field(self):
        data = {
            "email": "newcompany@example.com",
            "password": "StrongPass123"
            # Missing company_name
        }

        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("company_name", response.data)

    def test_register_company_duplicate_email(self):
        User.objects.create_user(email="existing@example.com", password="TestPass123", role=User.COMPANY)

        data = {
            "email": "existing@example.com",
            "password": "StrongPass123",
            "company_name": "Duplicate Company"
        }

        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class LoginAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = "/api/auth/login/"
        
        self.user = User.objects.create_user(
            email="user@example.com",
            password="TestPass123",
            role=User.COMPANY
        )

    def test_login_success(self):
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
        data = {
            "email": "user@example.com",
            "password": "WrongPass123"
        }

        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_login_nonexistent_user(self):
        data = {
            "email": "fakeuser@example.com",
            "password": "FakePass123"
        }

        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
