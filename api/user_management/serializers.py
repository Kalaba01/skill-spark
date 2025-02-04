from rest_framework import serializers
from authentication.models import User, Employee, Company, Admin

class EmployeeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Employee
        fields = ["id", "first_name", "last_name", "email"]

class CreateEmployeeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ["first_name", "last_name", "email", "password"]

    def create(self, validated_data):
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
    email = serializers.EmailField(required=False)

    class Meta:
        model = Employee
        fields = ["first_name", "last_name", "email"]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("email", None)

        if user_data:
            instance.user.email = user_data
            instance.user.save()

        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()
    working_at = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role", "company_name", "working_at"]

    def get_company_name(self, obj):
        if hasattr(obj, "company_profile"):
            return obj.company_profile.company_name
        return None

    def get_working_at(self, obj):
        if hasattr(obj, "employee_profile"):
            return obj.employee_profile.company.company_name
        return None

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    company_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "role", "company_name"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        role = validated_data.get("role")
        company_name = validated_data.pop("company_name", None)

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
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "role"]

    def update(self, instance, validated_data):
        old_role = instance.role
        new_role = validated_data.get("role", instance.role)

        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.role = new_role
        instance.save()

        if old_role != new_role:
            if old_role == User.ADMIN:
                Admin.objects.filter(user=instance).delete()
            elif old_role == User.COMPANY:
                Company.objects.filter(user=instance).delete()
            elif old_role == User.EMPLOYEE:
                Employee.objects.filter(user=instance).delete()

            if new_role == User.ADMIN:
                Admin.objects.create(user=instance)
            elif new_role == User.COMPANY:
                Company.objects.create(user=instance, company_name=f"Company of {instance.first_name} {instance.last_name}")
            elif new_role == User.EMPLOYEE:
                request = self.context.get("request")
                if request and hasattr(request.user, "company_profile"):
                    company = request.user.company_profile
                    Employee.objects.create(user=instance, company=company, first_name=instance.first_name, last_name=instance.last_name)
                else:
                    raise serializers.ValidationError("Employees can only be created by a company.")

        return instance
