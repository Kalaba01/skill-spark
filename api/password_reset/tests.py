from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core import mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class PasswordResetTests(TestCase):
    def setUp(self):
        """Set up test user and necessary variables for password reset tests."""
        self.client = APIClient()

        # Create a test user
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="OldPassword123",
            role=User.COMPANY
        )

        # Generate valid and invalid password reset tokens
        self.valid_uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.valid_token = default_token_generator.make_token(self.user)
        self.invalid_uidb64 = urlsafe_base64_encode(force_bytes(99999)) # Non-existent user ID
        self.invalid_token = "invalid-token"

    def test_request_password_reset_valid_email(self):
        """Test that a password reset request with a valid email sends a reset email."""
        response = self.client.post("/api/password-reset/", {"email": self.user.email})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1) # Ensure an email was sent
        self.assertIn("Reset Your Password", mail.outbox[0].subject)

        # Check if the email contains the reset link
        email_message = mail.outbox[0]
        found_reset_link = any(
            "http://localhost:3000/reset-password" in alternative[0]
            for alternative in email_message.alternatives
        )

        self.assertTrue(found_reset_link, "Reset link not found in email HTML content")

    def test_request_password_reset_invalid_email(self):
        """Test that requesting a password reset with a non-existent email does not send an email."""
        response = self.client.post("/api/password-reset/", {"email": "nonexistent@example.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 0) # No email should be sent

    def test_password_reset_valid_token(self):
        """Test that a valid password reset token allows a user to change their password."""
        new_password = "NewSecurePass123"
        response = self.client.post(f"/api/password-reset/confirm/{self.valid_uidb64}/{self.valid_token}/", {
            "password": new_password
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure the password was successfully changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))

    def test_password_reset_invalid_token(self):
        """Test that an invalid token prevents password reset."""
        new_password = "NewSecurePass123"
        response = self.client.post(f"/api/password-reset/confirm/{self.valid_uidb64}/{self.invalid_token}/", {
            "password": new_password
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid token", response.data["error"])

    def test_password_reset_missing_password(self):
        """Test that a password reset request without a password returns an error."""
        response = self.client.post(f"/api/password-reset/confirm/{self.valid_uidb64}/{self.valid_token}/", {})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Password field is required.", response.data["error"])
