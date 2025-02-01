from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Company

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "role", "first_name", "last_name", "is_active", "date_joined"]

class RegisterCompanySerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "company_name"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        company_name = validated_data.pop("company_name")

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            role=User.COMPANY
        )
        
        Company.objects.create(user=user, company_name=company_name)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        refresh = RefreshToken.for_user(user)

        refresh["user"] = UserSerializer(user).data

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(user).data
        }
