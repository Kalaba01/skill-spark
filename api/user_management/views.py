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
    UpdateUserSerializer,
    CompanyProfileSerializer
)


class EmployeeListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating employees.
    - Company users can view and add employees under their company.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Employee.objects.filter(company=self.request.user.company_profile)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateEmployeeSerializer
        return EmployeeSerializer

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company_profile)


class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting an employee.
    - Restricted to company users who own the employee's profile.
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = Employee.objects.all()
    serializer_class = UpdateEmployeeSerializer

    def get_object(self):
        employee = super().get_object()
        if employee.company != self.request.user.company_profile:
            raise PermissionDenied("Nemate dozvolu da upravljate ovim zaposlenim.")
        return employee


class UserListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating users.
    - Only admin users can access this endpoint.
    """

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


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a user.
    - Only admins can access this endpoint.
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer

    def get_object(self):
        user = super().get_object()
        if self.request.user.role != User.ADMIN:
            raise PermissionDenied("Nemate dozvolu za pregled ovog korisnika.")
        return user


class EmployeeProfileView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating an employee's profile.
    - Only authenticated employees can access their own profile.
    """

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
    """
    API view for generating a PDF report of an employee's activity.
    - Restricted to company users.
    - Includes employee details and passed quizzes.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        if not hasattr(request.user, "company_profile"):
            return HttpResponse(
                "You do not have permission to access this resource.", status=403
            )

        try:
            employee = Employee.objects.get(pk=pk, company=request.user.company_profile)
        except Employee.DoesNotExist:
            return HttpResponse(
                "Employee not found or you do not have access.", status=403
            )

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="{employee.first_name}_{employee.last_name}_report.pdf"'
        )

        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, height - 50, "Employee report")

        p.setFont("Helvetica", 12)
        p.drawString(100, height - 100, f"First Name: {employee.first_name}")
        p.drawString(100, height - 120, f"Last Name: {employee.last_name}")
        p.drawString(100, height - 140, f"Email: {employee.user.email}")
        p.drawString(100, height - 160, f"Company: {employee.company.company_name}")

        passed_quizzes = PassedQuizzes.objects.filter(employee=employee).select_related(
            "quiz"
        )
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


class CompanyProfileView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating a company's profile.
    - Only authenticated company users can access and modify their profile.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CompanyProfileSerializer

    def get_object(self):
        if not hasattr(self.request.user, "company_profile"):
            raise PermissionDenied(
                "You do not have permission to access this resource."
            )
        return self.request.user.company_profile

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
