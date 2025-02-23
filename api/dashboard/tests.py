from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import Company, Employee, Admin
from quizzes.models import Quiz

User = get_user_model()

# Base test case that sets up common data for all dashboard-related tests
class BaseDashboardTestCase(TestCase):
    def setUp(self):
        """Set up test users, company, employee, and quizzes before running tests."""
        self.client = APIClient()

         # Create an admin user
        self.admin_user = User.objects.create_user(
            email="admin@test.com", password="testpass", role=User.ADMIN
        )
        self.admin = Admin.objects.create(user=self.admin_user)

        # Create a company user
        self.company_user = User.objects.create_user(
            email="company@test.com", password="testpass", role=User.COMPANY
        )
        self.company = Company.objects.create(user=self.company_user, company_name="Test Company")

        # Create an employee user associated with the company
        self.employee_user = User.objects.create_user(
            email="employee@test.com", password="testpass", role=User.EMPLOYEE
        )
        self.employee = Employee.objects.create(
            user=self.employee_user, first_name="John", last_name="Doe", company=self.company
        )

        # Create quizzes for the company
        self.quiz1 = Quiz.objects.create(title="Quiz 1", company=self.company, duration=30, difficulty="easy")
        self.quiz2 = Quiz.objects.create(title="Quiz 2", company=self.company, duration=45, difficulty="medium")

# Tests for the Admin Dashboard API
class AdminDashboardTests(BaseDashboardTestCase):
    def setUp(self):
        """Initialize the API endpoint URL for admin dashboard statistics."""
        super().setUp()
        self.url = "/api/dashboard/admin-dashboard/"

    def test_admin_can_get_statistics(self):
        """Test if an admin can successfully retrieve system-wide statistics."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["admins"], 1)
        self.assertEqual(response.data["companies"], 1)
        self.assertEqual(response.data["employees"], 1)
        self.assertEqual(response.data["quizzes"], 2)

    def test_company_cannot_access_statistics(self):
        """Test that a company user is forbidden from accessing admin statistics."""
        self.client.force_authenticate(user=self.company_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_cannot_access_statistics(self):
        """Test that an employee user is forbidden from accessing admin statistics."""
        self.client.force_authenticate(user=self.employee_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_access_statistics(self):
        """Test that an unauthenticated request is rejected with a 401 status."""
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# Tests for the Company Dashboard API
class CompanyDashboardTests(BaseDashboardTestCase):
    def setUp(self):
        """Initialize the API endpoint URL for company dashboard statistics."""
        super().setUp()
        self.url = "/api/dashboard/company-dashboard/"

    def test_company_can_get_statistics(self):
        """Test if a company can retrieve its own statistics, including employee count and quizzes."""
        self.client.force_authenticate(user=self.company_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["employees"], 1)
        self.assertEqual(response.data["quizzes"], 2)

    def test_admin_cannot_access_company_statistics(self):
        """Test that an admin user is forbidden from accessing company-specific statistics."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_cannot_access_company_statistics(self):
        """Test that an employee is forbidden from accessing company-wide statistics."""
        self.client.force_authenticate(user=self.employee_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_access_company_statistics(self):
        """Test that an unauthenticated user is rejected with a 401 status."""
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# Tests for the Employee Dashboard API
class EmployeeDashboardTests(BaseDashboardTestCase):
    def setUp(self):
        """Initialize the API endpoint URL for employee dashboard statistics."""
        super().setUp()
        self.url = "/api/dashboard/employee-dashboard/"

    def test_employee_can_get_statistics(self):
        """Test if an employee can retrieve their own statistics, such as passed quizzes."""
        self.client.force_authenticate(user=self.employee_user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("passed_quizzes", response.data)
        self.assertIn("total_quizzes", response.data)
        self.assertEqual(response.data["total_quizzes"], 2)
        self.assertEqual(response.data["passed_quizzes"], 0) # Assuming no quizzes have been taken

    def test_admin_cannot_access_employee_statistics(self):
        """Test that an admin user is forbidden from accessing employee-specific statistics."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_company_cannot_access_employee_statistics(self):
        """Test that a company user is forbidden from accessing employee statistics."""
        self.client.force_authenticate(user=self.company_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_access_employee_statistics(self):
        """Test that an unauthenticated request is rejected with a 401 status."""
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
