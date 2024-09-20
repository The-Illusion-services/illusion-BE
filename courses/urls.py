from django.urls import path
from .views import CourseListAndCreate


urlpatterns = [
    path('course/', CourseListAndCreate.as_view(), name='course_create_and_list'),
]
