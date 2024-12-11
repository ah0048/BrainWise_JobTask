from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Custom permission to only allow admins to access the view.
    """
    def has_permission(self, request, view):
        return request.user.role == 'admin'

class IsAdminOrManager(BasePermission):
    """
    Custom permission to allow access for admin or manager.
    """
    def has_permission(self, request, view):
        # Allow if the user is admin or manager
        return request.user.role in ['admin', 'manager']

class IsAdminOrManagerOrEmployee(BasePermission):
    """
    Custom permission to allow access for admin, manager, or employee.
    """
    def has_permission(self, request, view):
        # Allow if the user is admin, manager, or employee
        return request.user.role in ['admin', 'manager', 'employee']
