from rest_framework import serializers
from authentication.models import User, Employee

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
