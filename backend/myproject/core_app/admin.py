from django.contrib import admin
from .models import User, Company, Department, Employee

# Register the models in the admin panel
admin.site.register(User)
admin.site.register(Company)
admin.site.register(Department)
admin.site.register(Employee)
