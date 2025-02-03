from django.urls import path
from .views import (
    AssignmentSubmissionCreateView, CertificationDetailView, CertificationListCreateView, CourseCreate, CourseDeleteView, CourseUpdateView,
    EnrollCourseView, EnrollmentListView, LessonListView,
    LessonProgressUpdateView, 
    ModuleCreateView, 
    ModuleListView, ModuleUpdateView,
    AssignmentCreateView,
    AssignmentUpdateView,
    AssignmentListView, QuizCreateView, QuizDetailView, QuizListView,
      QuizSubmissionView, ResourceCreateView, ResourceListView,
      AvailableCoursesList, UserCreatedCoursesList, UserEnrolledCoursesList
)

urlpatterns = [
    path('create-course/', CourseCreate.as_view(), name='course_create'),
    path('courses/', AvailableCoursesList.as_view(), name='available-courses'),
    path('courses/created/', UserCreatedCoursesList.as_view(), name='user-created-courses'),
    path('courses/enrolled/', UserEnrolledCoursesList.as_view(), name='user-enrolled-courses'),
    path('courses/<int:pk>/update/', CourseUpdateView.as_view(), name='course-update'),
    path('courses/<int:pk>/delete/', CourseDeleteView.as_view(), name='course-delete'),
    path('lessons/', LessonListView.as_view(), name='lesson_list'),
    path('create-module/', ModuleCreateView.as_view(), name='module_create'),
    path('update-module/<int:pk>/', ModuleUpdateView.as_view(), name='update_module'),
    path('modules/', ModuleListView.as_view(), name='module_list'),
    path('courses/<int:course_id>/assignments/', AssignmentListView.as_view(), name='assignment_list'),
    
    path('assignments/create/', AssignmentCreateView.as_view(), name='assignment_create'),
    path('assignments/update/<int:pk>/', AssignmentUpdateView.as_view(), name='assignment_update'),
    path('assignments/submit/', AssignmentSubmissionCreateView.as_view(), name='assignment_submit'),
    path('lessons/progress/<int:pk>/', LessonProgressUpdateView.as_view(), name='lesson_progress_update'),
    
    path('courses/enroll/', EnrollCourseView.as_view(), name='course_enroll'),
    path('courses/<int:course_id>/enrollments/', EnrollmentListView.as_view(), name='course-enrollments'),
    
    path('quizzes/', QuizListView.as_view(), name='quiz_list'),
    path('quizzes/create/', QuizCreateView.as_view(), name='quiz_create'),
    path('quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz_detail'),
    path('quizzes/submit/', QuizSubmissionView.as_view(), name='quiz_submit'),
    
    path('resources/', ResourceListView.as_view(), name='resource_list'),
    path('resources/create/', ResourceCreateView.as_view(), name='resource_create'),
    path('certifications/', CertificationListCreateView.as_view(), name='certification-list-create'),

    # Retrieve, update a certification
    path('certifications/<int:pk>/', CertificationDetailView.as_view(), name='certification-detail'),
]
