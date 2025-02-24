from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Custom user manager to handle user creation
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None, first_name=None, last_name=None):
        """
        Creates and returns a regular user with the given email, password, and role.
        """
        if not email:
            raise ValueError("The user must have an email address.")

        user = self.model(
            email=self.normalize_email(email),
            role=role,
            first_name=first_name or "",
            last_name=last_name or "",
            date_joined=now()
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and returns a superuser with the given email and password.
        """
        user = self.create_user(email, password, role="admin")
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


# Custom user model extending Django's AbstractBaseUser and PermissionsMixin
class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model supporting authentication via email instead of username.
    """

    # User role choices
    ADMIN = "admin"
    COMPANY = "company"
    EMPLOYEE = "employee"

    ROLE_CHOICES = [
        (ADMIN, "Admin"),
        (COMPANY, "Company"),
        (EMPLOYEE, "Employee"),
    ]

    # User fields
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=COMPANY)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=now)

    objects = UserManager()

    # Define email as the unique identifier for authentication
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"


# Admin model associated with the User model
class Admin(models.Model):
    """
    Represents an Admin user with extended functionalities.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="admin_profile")

    def __str__(self):
        return f"Admin: {self.user.email}"


# Company model associated with the User model
class Company(models.Model):
    """
    Represents a company within the system.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company_profile")
    company_name = models.CharField(max_length=255)

    def __str__(self):
        return self.company_name


# Employee model associated with the User and Company models
class Employee(models.Model):
    """
    Represents an employee associated with a company.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee_profile")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="employees")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.company.company_name})"
