from django.urls import path
from .views import ( 
    CourseCreate, CourseList, LessonListView, 
    ModuleCreateView, 
    ModuleListView, ModuleUpdateView,
    AssignmentCreateView,
    AssignmentUpdateView,
    AssignmentListView
)


urlpatterns = [
    path('create-course/', CourseCreate.as_view(), name='course_create'),
    path('courses/', CourseList.as_view(), name='course_list'),
    path('lessons/', LessonListView.as_view(), name='lesson_create'),
    path('create-module/', ModuleCreateView.as_view(), name='module_create'),
    path('update-module/<int:pk>/', ModuleUpdateView.as_view(), name='update-module'),
    path('modules/', ModuleListView.as_view(), name='module_list'),
    path('courses/<int:course_id>/assignments/', AssignmentListView.as_view(), name='assignment-list'),
    path('assignments/create/', AssignmentCreateView.as_view(), name='assignment-create'),
    path('assignments/update/<int:pk>/', AssignmentUpdateView.as_view(), name='assignment-update'),


]
