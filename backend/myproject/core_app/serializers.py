from rest_framework import serializers
from .models import Company, Department, Employee, User
from django.utils import timezone


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'num_departments', 'num_employees']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'company', 'name', 'num_employees']

class EmployeeSerializer(serializers.ModelSerializer):
    days_employed = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'company', 'department', 'status', 'name', 'email', 'mobile_number', 'address', 'designation', 'hired_on', 'days_employed']

    def get_days_employed(self, obj):
        # Calculate days employed based on the hired_on date
        if obj.hired_on:
            return (timezone.now().date() - obj.hired_on).days
        return 0

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}  # Ensure password is write-only

    def create(self, validated_data):
        # Hash the password before saving the user
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)  # Hash the password
        user.save()
        return user

    def update(self, instance, validated_data):
        # If password is provided, hash it
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
