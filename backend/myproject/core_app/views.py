from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from .models import Company, Department, Employee
from .serializers import CompanySerializer, DepartmentSerializer, EmployeeSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .permissions import IsAdmin, IsAdminOrManager, IsAdminOrManagerOrEmployee

# login view
@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=email, password=password)

    if user is not None:
        # Get or create a token for the user
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'userRole': user.role, 'userId': user.id}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

# logout view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        # Get the user's token from the request
        token = Token.objects.get(user=request.user)
        # Delete the token, effectively logging the user out
        token.delete()
        return Response({"message": "Logout successful"}, status=200)
    except Token.DoesNotExist:
        return Response({"error": "No active session found"}, status=400)


User = get_user_model()

# view to get all users
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    """
    Retrieve all users. Restricted to authenticated users.
    """
    if request.user.role != 'admin':
        return Response({"detail": "Not authorized to access this resource."}, status=status.HTTP_403_FORBIDDEN)

    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# view to get a specific user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request, id):
    """
    Retrieve details of a specific user.
    """
    try:
        user = User.objects.get(pk=id)
        if user != request.user and request.user.role != 'admin':
            return Response({"detail": "Not authorized to access this resource."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

# view to edit a specific user
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request, id):
    """
    Update details of a specific user.
    """
    try:
        user = User.objects.get(pk=id)
        if user != request.user and request.user.role != 'admin':
            return Response({"detail": "Not authorized to access this resource."}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        serializer = UserSerializer(user, data=data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)



# View to create a company (Admin only)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdmin])
def company_create(request):
    serializer = CompanySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View to get a list of all companies
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrManagerOrEmployee])
def company_list(request):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)

# View to get a single company
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrManagerOrEmployee])
def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)
    serializer = CompanySerializer(company)
    return Response(serializer.data)

# View to update company (Admin and Manager only)
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminOrManager])
def company_update(request, pk):
    company = get_object_or_404(Company, pk=pk)
    serializer = CompanySerializer(company, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View to delete company (Admin only)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdmin])
def company_delete(request, pk):
    company = get_object_or_404(Company, pk=pk)
    company.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# View to list all departments
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrManagerOrEmployee])
def department_list(request):
    departments = Department.objects.all()
    serializer = DepartmentSerializer(departments, many=True)
    return Response(serializer.data)

# View to get a single department
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrManagerOrEmployee])
def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    serializer = DepartmentSerializer(department)
    return Response(serializer.data)

# View to create a department (Admin only)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdmin])
def department_create(request):
    serializer = DepartmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View to update a department (Admin and Manager only)
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminOrManager])
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    serializer = DepartmentSerializer(department, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View to delete a department
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdmin])
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# View to list all employees
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrManagerOrEmployee])
def employee_list(request):
    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)

# View to get a single employee
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrManagerOrEmployee])
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    serializer = EmployeeSerializer(employee)
    return Response(serializer.data)

# View to create a new employee (Admin and Manager only)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminOrManager])
def employee_create(request):
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View to update an employee's data (Admin and Manager only)
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminOrManager])
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    serializer = EmployeeSerializer(employee, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View to delete an employee (Admin and Manager only)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminOrManager])
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
