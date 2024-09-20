from rest_framework.permissions import BasePermission

class IsEmployer(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and their role is 'Employer'
        return request.user.is_authenticated and request.user.role == 'Employer'
