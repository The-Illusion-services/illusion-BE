from .views import *

from django.urls import path
   
urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('google-signup/', GoogleSignUpView.as_view(), name='google-signup'),
    # path('google-login/', GoogleLogin.as_view(), name='google-login'),
    path('protected/', ProtectedView.as_view(), name='protected-view'),
]