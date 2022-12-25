from rest_framework import serializers
from .models import *
from django.contrib.auth.models import AnonymousUser, User
from rest_framework.authtoken.models import Token
from knox.models import AuthToken