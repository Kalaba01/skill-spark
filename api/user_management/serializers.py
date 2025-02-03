from rest_framework import serializers
from authentication.models import User, Employee

class EmployeeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Employee
        fields = ["id", "first_name", "last_name", "email"]

class CreateEmployeeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
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
            first_name=validated_data["first_name"], 
            last_name=validated_data["last_name"]
        )

        employee = Employee.objects.create(user=user, company=company, **validated_data)
        return employee

class UpdateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["first_name", "last_name"]

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()
        return instance
