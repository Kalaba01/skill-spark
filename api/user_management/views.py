from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from authentication.models import Employee, User
from .serializers import (
    EmployeeSerializer,
    CreateEmployeeSerializer,
    UpdateEmployeeSerializer,
    UserSerializer,
    CreateUserSerializer,
    UpdateUserSerializer
)

class EmployeeListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Employee.objects.filter(company=self.request.user.company_profile)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateEmployeeSerializer
        return EmployeeSerializer

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company_profile)

class UserListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != User.ADMIN:
            raise PermissionDenied("Nemate dozvolu za pregled svih korisnika.")
        return User.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateUserSerializer
        return UserSerializer

    def perform_create(self, serializer):
        if self.request.user.role != User.ADMIN:
            raise PermissionDenied("Samo administratori mogu kreirati korisnike.")
        serializer.save()

class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Employee.objects.all()
    serializer_class = UpdateEmployeeSerializer

    def get_object(self):
        employee = super().get_object()
        if employee.company != self.request.user.company_profile:
            raise PermissionDenied("Nemate dozvolu da upravljate ovim zaposlenim.")
        return employee

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer

    def get_object(self):
        user = super().get_object()
        if self.request.user.role != User.ADMIN:
            raise PermissionDenied("Nemate dozvolu za pregled ovog korisnika.")
        return user
