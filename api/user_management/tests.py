from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import Company, Employee, Admin

User = get_user_model()

class EmployeeManagementTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.company1_user = User.objects.create_user(email="company1@test.com", password="testpass", role=User.COMPANY)
        self.company1 = Company.objects.create(user=self.company1_user, company_name="Company One")

        self.company2_user = User.objects.create_user(email="company2@test.com", password="testpass", role=User.COMPANY)
        self.company2 = Company.objects.create(user=self.company2_user, company_name="Company Two")

        self.employee_user = User.objects.create_user(email="employee1@test.com", password="testpass", role=User.EMPLOYEE)
        self.employee1 = Employee.objects.create(user=self.employee_user, first_name="John", last_name="Doe", company=self.company1)

        self.client.force_authenticate(user=self.company1_user)

    def test_authentication_required(self):
        self.client.logout()
        response = self.client.get("/api/user-management/employees/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_employees(self):
        response = self.client.get("/api/user-management/employees/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["first_name"], "John")

    def test_create_employee(self):
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
        response = self.client.delete(f"/api/user-management/employees/{self.employee1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)

    def test_company_cannot_access_other_company_employees(self):
        self.client.force_authenticate(user=self.company2_user)
        response = self.client.get("/api/user-management/employees/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_company_cannot_delete_other_company_employee(self):
        self.client.force_authenticate(user=self.company2_user)
        response = self.client.delete(f"/api/user-management/employees/{self.employee1.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class UserManagementTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin_user = User.objects.create_user(email="admin@test.com", password="testpass", role=User.ADMIN)
        self.admin = Admin.objects.create(user=self.admin_user)

        self.company_user = User.objects.create_user(email="company@test.com", password="testpass", role=User.COMPANY)
        self.company = Company.objects.create(user=self.company_user, company_name="Test Company")

        self.employee_user = User.objects.create_user(email="employee@test.com", password="testpass", role=User.EMPLOYEE)
        self.employee = Employee.objects.create(user=self.employee_user, first_name="Jane", last_name="Doe", company=self.company)

        self.client.force_authenticate(user=self.admin_user)

    def test_list_users(self):
        response = self.client.get("/api/user-management/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 3)

    def test_create_admin(self):
        admin_data = {
            "email": "newadmin@test.com",
            "password": "testpass",
            "role": "admin"
        }
        response = self.client.post("/api/user-management/users/", admin_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(role=User.ADMIN).count(), 2)

    def test_create_company(self):
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
        update_data = {
            "email": "updatedadmin@test.com"
        }
        response = self.client.put(f"/api/user-management/users/{self.admin_user.id}/", update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.admin_user.refresh_from_db()
        self.assertEqual(self.admin_user.email, "updatedadmin@test.com")

    def test_edit_company(self):
        update_data = {
            "email": "updatedcompany@test.com",
            "company_name": "Updated Company Name"
        }
        response = self.client.put(f"/api/user-management/users/{self.company_user.id}/", update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.company.refresh_from_db()
        self.assertEqual(self.company.company_name, "Updated Company Name")

    def test_edit_employee(self):
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
        response = self.client.delete(f"/api/user-management/users/{self.employee_user.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 2)

    def test_cannot_change_user_role(self):
        update_data = {
            "role": "company"
        }
        response = self.client.put(f"/api/user-management/users/{self.employee_user.id}/", update_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
