from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import resolve
from .models import Posts


UserModel = get_user_model()


