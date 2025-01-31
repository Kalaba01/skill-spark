from django.contrib import admin
from .models import User, Company, Admin, Employee

admin.site.register(User)
admin.site.register(Company)
admin.site.register(Admin)
admin.site.register(Employee)
