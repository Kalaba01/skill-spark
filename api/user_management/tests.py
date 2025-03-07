from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import Company, Employee, Admin
from quizzes.models import PassedQuizzes, Quiz

User = get_user_model()

class EmployeeManagementTests(TestCase):
    """Test cases for managing employees within a company."""

    def setUp(self):
        """Set up test data for employee management."""
        self.client = APIClient()

        # Create two company users and their respective companies
        self.company1_user = User.objects.create_user(email="company1@test.com", password="testpass", role=User.COMPANY)
        self.company1 = Company.objects.create(user=self.company1_user, company_name="Company One")

        self.company2_user = User.objects.create_user(email="company2@test.com", password="testpass", role=User.COMPANY)
        self.company2 = Company.objects.create(user=self.company2_user, company_name="Company Two")

        # Create an employee under Company One
        self.employee_user = User.objects.create_user(email="employee1@test.com", password="testpass", role=User.EMPLOYEE)
        self.employee1 = Employee.objects.create(user=self.employee_user, first_name="John", last_name="Doe", company=self.company1)

        # Create a quiz and mark it as passed for the employee
        self.quiz = Quiz.objects.create(title="Test Quiz", company=self.company1, duration=30, difficulty="easy")
        PassedQuizzes.objects.create(employee=self.employee1, quiz=self.quiz)

        # Authenticate as company1 user
        self.client.force_authenticate(user=self.company1_user)

    def test_authentication_required(self):
        """Test that authentication is required to access the employee list."""
        self.client.logout()
        response = self.client.get("/api/user-management/employees/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_employees(self):
        """Test that a company can retrieve a list of its employees."""
        response = self.client.get("/api/user-management/employees/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["first_name"], "John")

    def test_create_employee(self):
        """Test that a company can add a new employee."""
        new_employee_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@test.com",
            "password": "testpass"
        }
        response = self.client.post("/api/user-management/employees/", new_employee_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)

    def test_edit_employee(self):
        """Test that a company can update an employee's details."""
        update_data = {
            "first_name": "Johnny",
            "last_name": "Doe",
            "email": "newemail@test.com"
        }
        response = self.client.put(f"/api/user-management/employees/{self.employee1.id}/", update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.employee1.refresh_from_db()
        self.assertEqual(self.employee1.first_name, "Johnny")
        self.assertEqual(self.employee1.user.email, "newemail@test.com")

    def test_delete_employee(self):
        """Test that a company can remove an employee."""
        response = self.client.delete(f"/api/user-management/employees/{self.employee1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)

    def test_company_cannot_access_other_company_employees(self):
        """Test that a company cannot access another company's employees."""
        self.client.force_authenticate(user=self.company2_user)
        response = self.client.get("/api/user-management/employees/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_company_cannot_delete_other_company_employee(self):
        """Test that a company cannot delete an employee from another company."""
        self.client.force_authenticate(user=self.company2_user)
        response = self.client.delete(f"/api/user-management/employees/{self.employee1.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_employee_has_passed_quizzes(self):
        """Test that an employee's passed quizzes are listed."""
        response = self.client.get("/api/user-management/employees/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn("passed_quizzes", response.data[0])
        self.assertEqual(len(response.data[0]["passed_quizzes"]), 1)
        self.assertEqual(response.data[0]["passed_quizzes"][0]["title"], "Test Quiz")

    def test_employee_with_no_passed_quizzes(self):
        """Test that an employee with no passed quizzes is returned correctly."""
        new_employee_user = User.objects.create_user(email="employee2@test.com", password="testpass", role=User.EMPLOYEE)
        new_employee = Employee.objects.create(user=new_employee_user, first_name="Jane", last_name="Doe", company=self.company1)

        response = self.client.get("/api/user-management/employees/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        employee_data = next(emp for emp in response.data if emp["first_name"] == "Jane")
        self.assertIn("passed_quizzes", employee_data)
        self.assertEqual(len(employee_data["passed_quizzes"]), 0)


class UserManagementTests(TestCase):
    """Test cases for user management by an admin."""

    def setUp(self):
        """Set up test data for user management tests."""
        self.client = APIClient()

        # Create an admin user
        self.admin_user = User.objects.create_user(email="admin@test.com", password="testpass", role=User.ADMIN)
        self.admin = Admin.objects.create(user=self.admin_user)

        # Create a company user
        self.company_user = User.objects.create_user(email="company@test.com", password="testpass", role=User.COMPANY)
        self.company = Company.objects.create(user=self.company_user, company_name="Test Company")

        # Create an employee under the company
        self.employee_user = User.objects.create_user(email="employee@test.com", password="testpass", role=User.EMPLOYEE)
        self.employee = Employee.objects.create(user=self.employee_user, first_name="Jane", last_name="Doe", company=self.company)

        # Authenticate as admin
        self.client.force_authenticate(user=self.admin_user)

    def test_list_users(self):
        """Test that an admin can retrieve a list of all users."""
        response = self.client.get("/api/user-management/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 3)

    def test_create_admin(self):
        """Test that an admin can create another admin user."""
        admin_data = {
            "email": "newadmin@test.com",
            "password": "testpass",
            "role": "admin"
        }
        response = self.client.post("/api/user-management/users/", admin_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(role=User.ADMIN).count(), 2)

    def test_create_company(self):
        """Test that an admin can create a new company."""
        company_data = {
            "email": "newcompany@test.com",
            "password": "testpass",
            "role": "company",
            "company_name": "New Company"
        }
        response = self.client.post("/api/user-management/users/", company_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 2)

    def test_create_employee(self):
        """Test that an admin can create a new employee for a company."""
        employee_data = {
            "first_name": "New",
            "last_name": "Employee",
            "email": "newemployee@test.com",
            "password": "testpass",
            "role": "employee",
            "company_name": "Test Company"
        }
        response = self.client.post("/api/user-management/users/", employee_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)

    def test_edit_admin(self):
        """Test that an admin can update another admin's email."""
        update_data = {
            "email": "updatedadmin@test.com"
        }
        response = self.client.put(f"/api/user-management/users/{self.admin_user.id}/", update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.admin_user.refresh_from_db()
        self.assertEqual(self.admin_user.email, "updatedadmin@test.com")

    def test_edit_company(self):
        """Test that an admin can update a company's email and name."""
        update_data = {
            "email": "updatedcompany@test.com",
            "company_name": "Updated Company Name"
        }
        response = self.client.put(f"/api/user-management/users/{self.company_user.id}/", update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.company.refresh_from_db()
        self.assertEqual(self.company.company_name, "Updated Company Name")

    def test_edit_employee(self):
        """Test that an admin can update an employee's details."""
        update_data = {
            "first_name": "Updated",
            "last_name": "Employee",
            "email": "updatedemployee@test.com",
            "company_name": "Test Company"
        }
        response = self.client.put(f"/api/user-management/users/{self.employee_user.id}/", update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.employee.refresh_from_db()
        self.assertEqual(self.employee.first_name, "Updated")
        self.assertEqual(self.employee.user.email, "updatedemployee@test.com")

    def test_delete_user(self):
        """Test that an admin can delete a user."""
        response = self.client.delete(f"/api/user-management/users/{self.employee_user.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 2)

    def test_cannot_change_user_role(self):
        """Test that an admin cannot change a user's role."""
        update_data = {
            "role": "company"
        }
        response = self.client.put(f"/api/user-management/users/{self.employee_user.id}/", update_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EmployeeProfileTests(TestCase):
    """Test cases for employee profile management."""

    def setUp(self):
        """Set up test data for employee profile tests."""
        self.client = APIClient()

        # Create a company and its associated user
        self.company = Company.objects.create(
            user=User.objects.create_user(
                email="company@test.com", password="testpass", role=User.COMPANY
            ),
            company_name="Test Company"
        )

        # Create an employee user
        self.employee_user = User.objects.create_user(
            email="employee@test.com",
            password="testpass",
            role=User.EMPLOYEE
        )

        # Assign employee to the company
        self.employee = Employee.objects.create(
            user=self.employee_user,
            first_name="John",
            last_name="Doe",
            company=self.company
        )

        # Authenticate as the employee
        self.client.force_authenticate(user=self.employee_user)

    def test_get_employee_profile(self):
        """Test that an employee can retrieve their profile."""
        response = self.client.get("/api/user-management/employee-profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "John")
        self.assertEqual(response.data["last_name"], "Doe")
        self.assertEqual(response.data["email"], "employee@test.com")
        self.assertEqual(response.data["working_at"], "Test Company")

    def test_update_employee_profile(self):
        """Test that an employee can update their profile information."""
        updated_data = {
            "first_name": "Johnny",
            "last_name": "Smith",
            "email": "johnny.smith@test.com"
        }
        response = self.client.post("/api/user-management/employee-profile/", updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.employee.refresh_from_db()
        self.employee.user.refresh_from_db()
        self.assertEqual(self.employee.first_name, "Johnny")
        self.assertEqual(self.employee.last_name, "Smith")
        self.assertEqual(self.employee.user.email, "johnny.smith@test.com")

    def test_update_employee_profile_invalid_email(self):
        """Test that an employee cannot update their profile with an invalid email."""
        invalid_data = {
            "first_name": "Johnny",
            "last_name": "Smith",
            "email": "invalid-email"
        }
        response = self.client.post("/api/user-management/employee-profile/", invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_access(self):
        """Test that an unauthorized user cannot access employee profile endpoints."""
        self.client.logout()
        response = self.client.get("/api/user-management/employee-profile/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post("/api/user-management/employee-profile/", {"first_name": "New Name"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class EmployeeReportTests(TestCase):
    """Test cases for generating employee reports."""

    def setUp(self):
        """Set up test data for employee report generation tests."""
        self.client = APIClient()

        # Create two companies
        self.company1_user = User.objects.create_user(email="company1@test.com", password="testpass", role=User.COMPANY)
        self.company1 = Company.objects.create(user=self.company1_user, company_name="Company One")

        self.company2_user = User.objects.create_user(email="company2@test.com", password="testpass", role=User.COMPANY)
        self.company2 = Company.objects.create(user=self.company2_user, company_name="Company Two")

        # Create an employee for Company One
        self.employee_user = User.objects.create_user(email="employee1@test.com", password="testpass", role=User.EMPLOYEE)
        self.employee1 = Employee.objects.create(user=self.employee_user, first_name="John", last_name="Doe", company=self.company1)

        # Authenticate as the first company's user
        self.client.force_authenticate(user=self.company1_user)

    def test_generate_employee_report(self):
        """Test that a company can generate a PDF report for an employee."""
        response = self.client.get(f"/api/user-management/employees/{self.employee1.id}/report/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")

    def test_employee_cannot_generate_report(self):
        """Test that an employee cannot generate their own report."""
        self.client.force_authenticate(user=self.employee_user)
        response = self.client.get(f"/api/user-management/employees/{self.employee1.id}/report/")
        self.assertEqual(response.status_code, 403)

    def test_company_cannot_generate_report_for_other_company_employee(self):
        """Test that a company cannot generate a report for another company's employee."""
        self.client.force_authenticate(user=self.company2_user)
        response = self.client.get(f"/api/user-management/employees/{self.employee1.id}/report/")
        self.assertEqual(response.status_code, 403)


class CompanyProfileTests(TestCase):
    """Test cases for company profile management."""

    def setUp(self):
        """Set up test data for company profile tests."""
        self.client = APIClient()

        # Create two company users
        self.company_user = User.objects.create_user(
            email="company@test.com",
            password="testpass",
            role=User.COMPANY
        )
        self.company = Company.objects.create(
            user=self.company_user,
            company_name="Test Company"
        )

        self.other_company_user = User.objects.create_user(
            email="othercompany@test.com",
            password="testpass",
            role=User.COMPANY
        )
        self.other_company = Company.objects.create(
            user=self.other_company_user,
            company_name="Other Company"
        )

         # Create an admin user
        self.admin_user = User.objects.create_user(
            email="admin@test.com",
            password="testpass",
            role=User.ADMIN
        )

        # Create an employee user
        self.employee_user = User.objects.create_user(
            email="employee@test.com",
            password="testpass",
            role=User.EMPLOYEE
        )

        # Define company profile API endpoint
        self.company_profile_url = "/api/user-management/company-profile/"

    def test_company_can_get_profile(self):
        """Test that a company can retrieve its profile information."""
        self.client.force_authenticate(user=self.company_user)
        response = self.client.get(self.company_profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["company_name"], "Test Company")
        self.assertEqual(response.data["email"], "company@test.com")

    def test_company_can_update_profile(self):
        """Test that a company can update its profile details."""
        self.client.force_authenticate(user=self.company_user)
        updated_data = {
            "company_name": "Updated Company Name",
            "email": "updatedcompany@test.com"
        }
        response = self.client.post(self.company_profile_url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.company.refresh_from_db()
        self.assertEqual(self.company.company_name, "Updated Company Name")
        self.assertEqual(self.company.user.email, "updatedcompany@test.com")
    
    def test_admin_cannot_access_company_profile(self):
        """Test that an admin cannot access company profile endpoints."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.company_profile_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_cannot_access_company_profile(self):
        """Test that an employee cannot access company profile endpoints."""
        self.client.force_authenticate(user=self.employee_user)
        response = self.client.get(self.company_profile_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_user_cannot_access_company_profile(self):
        """Test that an unauthenticated user cannot access company profile endpoints."""
        self.client.logout()
        response = self.client.get(self.company_profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_email_update(self):
        """Test that a company cannot update its profile with an invalid email."""
        self.client.force_authenticate(user=self.company_user)
        invalid_data = {
            "company_name": "Valid Name",
            "email": "invalid-email"
        }
        response = self.client.post(self.company_profile_url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
