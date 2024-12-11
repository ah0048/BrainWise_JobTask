from django.urls import path
from . import views

urlpatterns = [
    # Company URLs
    path('companies/', views.company_list, name='company-list'),
    path('companies/<int:pk>/', views.company_detail, name='company-detail'),
    path('companies/<int:pk>/update/', views.company_update, name='company-update'),
    path('companies/<int:pk>/delete/', views.company_delete, name='company-delete'),

    # Department URLs
    path('departments/', views.department_list, name='department-list'),
    path('departments/<int:pk>/', views.department_detail, name='department-detail'),
    path('departments/create/', views.department_create, name='department-create'),
    path('departments/<int:pk>/update/', views.department_update, name='department-update'),
    path('departments/<int:pk>/delete/', views.department_delete, name='department-delete'),

    # Employee URLs
    path('employees/', views.employee_list, name='employee-list'),
    path('employees/<int:pk>/', views.employee_detail, name='employee-detail'),
    path('employees/create/', views.employee_create, name='employee-create'),
    path('employees/<int:pk>/update/', views.employee_update, name='employee-update'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee-delete'),
]
