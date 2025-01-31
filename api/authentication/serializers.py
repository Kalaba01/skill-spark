from rest_framework import serializers
from .models import User, Company

class RegisterCompanySerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    company_name = serializers.CharField(write_only=True)

    class Meta:
        model = Company
        fields = ['email', 'password', 'company_name']

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        company_name = validated_data['company_name']

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            role=User.COMPANY
        )

        company = Company.objects.create(user=user, company_name=company_name)
        return company
