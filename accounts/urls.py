from .views import *

from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from jobs.views import JobViewSet, ApplicationViewSet

router = DefaultRouter()
router.register(r'jobs', JobViewSet)
router.register(r'applications', ApplicationViewSet)
   
urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path("glogin/", LoginPage.as_view(), name="login"),
    
    path("v1/auth/google/", GoogleLogin.as_view(), name="google_login"),
    path(
        "v1/auth/google/callback/",
        GoogleLoginCallback.as_view(),
        name="google_login_callback",
    ),



    path('profile/', ProfileView.as_view(), name='profile'),
    path('', include(router.urls)),
    

    path('profile/<int:id>', ProfileView.as_view(), name='profile'),

]