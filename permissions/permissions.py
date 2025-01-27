from rest_framework.permissions import BasePermission

class IsCreator(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and their role is 'Creator'
        return request.user.is_authenticated and request.user.role == 'Creator'

class IsLearner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Learner'