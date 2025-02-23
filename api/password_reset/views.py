from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib.auth import get_user_model
from .serializers import PasswordResetRequestSerializer


User = get_user_model()

class RequestPasswordResetView(APIView):
    """
    API view for requesting a password reset link.
    - Generates a unique token and encodes the user's ID.
    - Sends an email containing the password reset link.
    """
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"http://localhost:3000/reset-password/{uidb64}/{token}"

            email_content = render_to_string("password_reset_email.html", {"reset_link": reset_link})

            send_mail(
                "Reset Your Password",
                "",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=email_content,
                fail_silently=False
            )

        return Response({"message": "A password reset link has been sent to your email."}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    """
    API view for confirming a password reset.
    - Verifies the provided token and user ID.
    - Updates the user's password upon successful validation.
    """
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            if not default_token_generator.check_token(user, token):
                return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

            new_password = request.data.get("password")
            if not new_password:
                return Response({"error": "Password field is required."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)

        except (User.DoesNotExist, ValueError, TypeError):
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
