from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from .models import Course, Module, Lesson, Assignment

class CourseAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.course_data = {
            'course_title': 'Django for Beginners',
            'course_description': 'A comprehensive course on Django.',
            'course_language': 'English',
            'course_level': 'Beginner',
            'course_category': 'Web3 Expert',
            'price': 100.00,
            'certification': True,
            'difficulty_level': 'beginner',
            'estimated_duration': 10,
            'created_by': self.user.id,
        }
    
    def test_create_course(self):
        response = self.client.post(reverse('course-list'), self.course_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Course.objects.get().course_title, 'Django for Beginners')

    def test_list_courses(self):
        Course.objects.create(**self.course_data)
        response = self.client.get(reverse('course-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class ModuleAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.course = Course.objects.create(course_title='Django for Beginners', created_by=self.user)
        self.module_data = {
            'title': 'Introduction',
            'course': self.course.id,
        }

    def test_create_module(self):
        response = self.client.post(reverse('module-list'), self.module_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Module.objects.count(), 1)
        self.assertEqual(Module.objects.get().title, 'Introduction')

class LessonAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.course = Course.objects.create(course_title='Django for Beginners', created_by=self.user)
        self.module = Module.objects.create(title='Introduction', course=self.course)
        self.lesson_data = {
            'module': self.module.id,
            'title': 'Getting Started',
            'description': 'Learn the basics.',
            'is_published': True,
        }

    def test_create_lesson(self):
        response = self.client.post(reverse('lesson-list'), self.lesson_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(Lesson.objects.get().title, 'Getting Started')

class AssignmentAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.course = Course.objects.create(course_title='Django for Beginners', created_by=self.user)
        self.assignment_data = {
            'title': 'First Assignment',
            'description': 'Complete the first assignment.',
            'course': self.course.id,
            'due_date': '2023-12-31',
            'created_by': self.user.id,
        }

    def test_create_assignment(self):
        response = self.client.post(reverse('assignment-list'), self.assignment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Assignment.objects.count(), 1)
        self.assertEqual(Assignment.objects.get().title, 'First Assignment')



