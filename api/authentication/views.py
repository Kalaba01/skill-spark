from rest_framework import generics
from .serializers import RegisterCompanySerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status


class RegisterCompanyView(generics.CreateAPIView):
    """
    API view for registering a company.
    Uses RegisterCompanySerializer to validate and create a new company user.
    """

    serializer_class = RegisterCompanySerializer

    def create(self, request, *args, **kwargs):
        """
        Handles the creation of a new company user.

        - Validates request data using `RegisterCompanySerializer`.
        - If valid, saves the user and returns a success message.
        - If invalid, returns an error response.
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "Company registered successfully!"},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    """
    API view for user login.
    Uses LoginSerializer to authenticate users and return JWT tokens.
    """

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Handles user authentication.

        - Validates login credentials.
        - If valid, returns access and refresh tokens along with user details.
        - If invalid, returns an error response.
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
