from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Company

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    Returns user-related information.
    """
    class Meta:
        model = User
        fields = ["id", "email", "role", "first_name", "last_name", "is_active", "date_joined"]

class RegisterCompanySerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new company.
    - Creates a user with the COMPANY role.
    - Creates an associated Company object.
    - Sends a welcome email upon successful registration.
    """
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
        
        company = Company.objects.create(user=user, company_name=company_name)

        self.send_welcome_email(user.email, company_name)

        return user

    def send_welcome_email(self, email, company_name):
        """
        Sends a welcome email to the newly registered company.
        """
        subject = "Welcome to SkillSpark!"
        email_content = render_to_string("welcome_email.html", {"company_name": company_name})
        
        send_mail(
            subject,
            "",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            html_message=email_content,
            fail_silently=False
        )

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user authentication.
    - Validates user credentials.
    - Generates and returns JWT tokens upon successful login.
    """
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
