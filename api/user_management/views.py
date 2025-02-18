from django.http import HttpResponse
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from authentication.models import Employee, User
from quizzes.models import PassedQuizzes
from .serializers import (
    EmployeeSerializer,
    EmployeeProfileSerializer,
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

class EmployeeProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmployeeProfileSerializer

    def get_object(self):
        if not hasattr(self.request.user, "employee_profile"):
            raise PermissionDenied("Nemate dozvolu za pristup ovom resursu.")
        return self.request.user.employee_profile

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class GenerateEmployeeReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk, company=request.user.company_profile)
        except Employee.DoesNotExist:
            return HttpResponse("You do not have permission to access this resource.", status=403)

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{employee.first_name}_{employee.last_name}_report.pdf"'

        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, height - 50, "Employee report")

        p.setFont("Helvetica", 12)
        p.drawString(100, height - 100, f"First Name: {employee.first_name}")
        p.drawString(100, height - 120, f"Last Name: {employee.last_name}")
        p.drawString(100, height - 140, f"Email: {employee.user.email}")
        p.drawString(100, height - 160, f"Company: {employee.company.company_name}")

        passed_quizzes = PassedQuizzes.objects.filter(employee=employee).select_related("quiz")
        p.drawString(100, height - 200, "Quizzes passed:")

        if passed_quizzes.exists():
            y_position = height - 220
            for pq in passed_quizzes:
                p.drawString(120, y_position, f"- {pq.quiz.title}")
                y_position -= 20
        else:
            p.drawString(120, height - 220, "No quizzes passed.")

        p.showPage()
        p.save()
        return response
