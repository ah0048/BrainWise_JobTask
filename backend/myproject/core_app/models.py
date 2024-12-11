from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('employee', 'Employee')
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    num_departments = models.PositiveIntegerField(default=0)
    num_employees = models.PositiveIntegerField(default=0)

    def update_counts(self):
        """Update department and employee counts"""
        self.num_departments = self.department_set.count()
        self.num_employees = self.employee_set.count()
        self.save()

    def __str__(self):
        return self.name

class Department(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=100)
    num_employees = models.PositiveIntegerField(default=0)

    def update_employee_count(self):
        """Update employee count in department"""
        self.num_employees = self.employee_set.count()
        self.save()
        # Also update parent company's employee count
        self.company.update_counts()

    def __str__(self):
        return f"{self.name} - {self.company.name}"

    class Meta:
        unique_together = ('company', 'name')

class Employee(models.Model):
    EMPLOYEE_STATUS = [
        ('application_received', 'Application Received'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('hired', 'Hired'),
        ('not_accepted', 'Not Accepted')
    ]

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees')
    
    status = models.CharField(max_length=30, choices=EMPLOYEE_STATUS, default='application_received')
    
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(validators=[phone_regex], max_length=16)
    address = models.TextField()
    designation = models.CharField(max_length=100)
    
    hired_on = models.DateField(null=True, blank=True)
    days_employed = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        # Calculate days employed if hired
        if self.hired_on:
            self.days_employed = (timezone.now().date() - self.hired_on).days
        
        # Validate department belongs to selected company
        if self.department.company != self.company:
            raise ValueError("Department must belong to the selected company")
        
        super().save(*args, **kwargs)
        
        # Update counts in department and company
        self.department.update_employee_count()

    def __str__(self):
        return f"{self.name} - {self.designation}"
