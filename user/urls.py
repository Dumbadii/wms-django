from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('user/register/', views.Register.as_view()),
    # path('users/login/', views.Login.as_view()),
    path('user/token/', obtain_auth_token)
]