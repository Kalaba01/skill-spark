from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ADMIN = 'admin'
    COMPANY = 'company'
    EMPLOYEE = 'employee'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (COMPANY, 'Company'),
        (EMPLOYEE, 'Employee')
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=COMPANY)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True
    )

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
    company_name = models.CharField(max_length=255)

    def __str__(self):
        return self.company_name


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin')

    def __str__(self):
        return f"Admin: {self.user.email}"


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.company.company_name})"
