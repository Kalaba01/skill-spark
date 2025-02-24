from rest_framework import serializers
from authentication.models import User, Employee, Company, Admin
from quizzes.models import PassedQuizzes, Quiz

class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for employee data.
    - Includes basic employee details and a list of passed quizzes.
    """
    email = serializers.EmailField(source="user.email", read_only=True)
    passed_quizzes = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ["id", "first_name", "last_name", "email", "passed_quizzes"]

    def get_passed_quizzes(self, obj):
        """
        Retrieves a list of quizzes an employee has passed.
        """
        quizzes = Quiz.objects.filter(
            passed_by_employees__employee=obj
        ).values("id", "title")
        return list(quizzes)

class CreateEmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for creating an employee.
    - Requires email and password input.
    - Associates the employee with the company of the authenticated user.
    """
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ["first_name", "last_name", "email", "password"]

    def create(self, validated_data):
        """
        Creates an employee with a new user account.
        - Links the employee to the requesting company's profile.
        """
        company = self.context["request"].user.company_profile
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        user = User.objects.create_user(
            email=email,
            password=password,
            role=User.EMPLOYEE,
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", "")
        )

        employee = Employee.objects.create(
            user=user,
            company=company,
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", "")
        )

        return employee

class UpdateEmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for updating employee details.
    - Allows modification of first name, last name, and email.
    """
    email = serializers.EmailField(required=False)

    class Meta:
        model = Employee
        fields = ["first_name", "last_name", "email"]

    def update(self, instance, validated_data):
        """
        Updates the employee's information.
        """
        user_data = validated_data.pop("email", None)

        if user_data:
            instance.user.email = user_data
            instance.user.save()

        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving user details.
    - Includes company name and workplace information.
    """
    company_name = serializers.SerializerMethodField()
    working_at = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role", "company_name", "working_at"]

    def get_company_name(self, obj):
        """
        Retrieves the company name for a company user.
        """
        if hasattr(obj, "company_profile"):
            return obj.company_profile.company_name
        return None

    def get_working_at(self, obj):
        """
        Retrieves the company where an employee is working.
        """
        if hasattr(obj, "employee_profile"):
            return obj.employee_profile.company.company_name
        return None

class CreateUserSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new users.
    - Supports multiple roles (Admin, Company, Employee).
    - Employees must be assigned to a company.
    """
    password = serializers.CharField(write_only=True)
    company_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "role", "company_name"]

    def create(self, validated_data):
        """
        Creates a new user with the given role.
        - Admins and Companies can be created directly.
        - Employees must be linked to an existing company.
        """
        password = validated_data.pop("password")
        role = validated_data.get("role")
        company_name = validated_data.pop("company_name", None)

        if company_name == "":
            company_name = None

        user = User.objects.create_user(**validated_data, password=password)

        if role == User.ADMIN:
            Admin.objects.create(user=user)
        elif role == User.COMPANY:
            Company.objects.create(user=user, company_name=company_name or f"Company of {user.first_name} {user.last_name}")
        elif role == User.EMPLOYEE:
            if not company_name:
                raise serializers.ValidationError("Employee must be assigned to a company.")
            company = Company.objects.filter(company_name=company_name).first()
            if not company:
                raise serializers.ValidationError("Invalid company.")
            Employee.objects.create(user=user, company=company, first_name=user.first_name, last_name=user.last_name)

        return user

class UpdateUserSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user details.
    - Allows modification of email, name, and company assignment.
    """
    company_name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "company_name"]

    def update(self, instance, validated_data):
        """
        Updates user details based on role.
        - Employees and companies can modify their company assignments.
        """
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)

        if instance.role == User.EMPLOYEE and hasattr(instance, "employee_profile"):
            instance.employee_profile.first_name = validated_data.get("first_name", instance.employee_profile.first_name)
            instance.employee_profile.last_name = validated_data.get("last_name", instance.employee_profile.last_name)
            instance.employee_profile.save()

        if instance.role == User.COMPANY and "company_name" in validated_data:
            if hasattr(instance, "company_profile"):
                instance.company_profile.company_name = validated_data["company_name"]
                instance.company_profile.save()

        if instance.role == User.EMPLOYEE and "company_name" in validated_data:
            company = Company.objects.filter(company_name=validated_data["company_name"]).first()
            if company:
                if hasattr(instance, "employee_profile"):
                    instance.employee_profile.company = company
                    instance.employee_profile.save()
            else:
                raise serializers.ValidationError({"company_name": "Selected company does not exist."})

        instance.save()
        return instance

class EmployeeProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving and updating an employee's profile.
    - Includes email and company information.
    """
    email = serializers.EmailField(source="user.email", read_only=False)
    working_at = serializers.CharField(source="company.company_name", read_only=True)

    class Meta:
        model = Employee
        fields = ["first_name", "last_name", "email", "working_at"]

    def update(self, instance, validated_data):
        """
        Updates the employee profile.
        """
        user_data = validated_data.pop("user", {})
        if "email" in user_data:
            instance.user.email = user_data["email"]
            instance.user.save()

        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()
        return instance

class CompanyProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for company profile data.
    - Includes company name, email, number of employees, and number of quizzes.
    """
    email = serializers.EmailField(source="user.email", read_only=False)
    employee_count = serializers.SerializerMethodField()
    quiz_count = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ["company_name", "email", "employee_count", "quiz_count"]

    def get_employee_count(self, obj):
        """
        Retrieves the number of employees in the company.
        """
        return obj.employees.count()

    def get_quiz_count(self, obj):
        """
        Retrieves the number of quizzes created by the company.
        """
        return Quiz.objects.filter(company=obj).count()

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        
        if "email" in user_data:
            instance.user.email = user_data["email"]
            instance.user.save()

        instance.company_name = validated_data.get("company_name", instance.company_name)
        instance.save()
        return instance
