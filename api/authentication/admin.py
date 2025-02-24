from django.contrib import admin
from .models import User, Company, Admin, Employee

admin.site.register(User) # Register the User model
admin.site.register(Company) # Register the Company model
admin.site.register(Admin) # Register the Admin model
admin.site.register(Employee) # Register the Employee model
