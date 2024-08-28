from django.urls import path
from rest_framework import routers

from user.views import UserRegistrationView

router = routers.DefaultRouter()


urlpatterns = [
    path('user/', UserRegistrationView.as_view(), name='user')
]
