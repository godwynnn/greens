from django.contrib import admin
from django.urls import path
from django.urls import include, re_path

from rest_framework.routers import DefaultRouter
from .views import *



urlpatterns = [
    path('', SocialsView.as_view(),name='social'),
    path('social/<str:pk>/', SocialDetailUpdateView.as_view(),name='social_detail'),
    path('social/<str:post_type>', CategoryView.as_view(),name='category'),
    path('social/like/<str:id>/', LikeUnlikeView.as_view(),name='like_unlike'),
    path('social/comment/<str:id>/', CommentView.as_view(),name='comments'),
    # path('social/user/location/',MapView.as_view(),name='location')
]
