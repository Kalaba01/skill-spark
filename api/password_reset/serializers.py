from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for password reset request.
    - Validates that the email exists in the system.
    - Prevents revealing whether an email is registered.
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("If this email exists, a reset link has been sent.")
        return value
