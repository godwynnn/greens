from rest_framework import serializers
from .models import *
from django.contrib.auth.models import AnonymousUser, User
from rest_framework.authtoken.models import Token
from knox.models import AuthToken





class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Userprofile
        fields=['user','image']


class PostTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=PostType
        fields=['type','catergories']
    



class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model=Social
        fields='__all__'




class LikeUnlikeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Social
        fields=['likes']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields="__all__"


# class MapSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Maps
#         fields="__all__"