from django.shortcuts import render
from greensapp.models import *
from greensapp.serializers import *
from knox.auth import TokenAuthentication 
from knox.models import AuthToken
from rest_framework import generics
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password, make_password
import datetime
import pytz
from django.utils import timezone
from django.core.mail import send_mass_mail

from re import L
from time import timezone
from urllib import response

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,RetrieveAPIView,ListCreateAPIView,RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from .paginator import CustomPagination
# Create your views here.



def GetPostType(request):
    post_type=request.data.get('post_type')
    try:
        type_name=PostType.objects.get(type__iexact=post_type)
    except ObjectDoesNotExist:
        type_name=None
    
    return type_name


def GetUserByComment(comment):

    try:
        pass
    except:
        pass


def getfilters(request,*args,**kwargs):
    if request.method == 'POST':
        generalfilters = dict(request.POST)
    else:
        generalfilters = dict(request.GET)
    exclude_contain_words = []
    filters = {}
    try:
        model_fields = kwargs['model_fields']
    except KeyError:
        model_fields = []
    try:
        exclude_list = kwargs['exclude']
    except KeyError:
        exclude_list = []

    try:
        contain_words_list = kwargs['contain_words']
    except KeyError:
        contain_words_list =[]
    for filter in generalfilters:
        if filter =='format':
            exclude_contain_words.append(filter)
        elif filter in exclude_list:
            exclude_contain_words.append(filter)
        elif not generalfilters[filter][0]:
            exclude_contain_words.append(filter)
        elif filter not in model_fields:
            for word in model_fields:
                    if filter.find(word) != -1:                
                        exclude_contain_words.append(filter)
        else:
            for word in contain_words_list:
                if (word and filter not in exclude_contain_words):
                    if filter.find(word) != -1:                
                        exclude_contain_words.append(filter)
        if filter in exclude_contain_words:
            pass
        else:
            # exist = (filter in args) or (filter in kwargs['model_fields'])
            filter = str(filter)
            filters[filter] = generalfilters[filter][0]
    return filters


class SocialsView(APIView):
    queryset=Social.objects.all()
    serializer_class=SocialSerializer
    authentication_classes =[TokenAuthentication,]
    pagination_class = CustomPagination 


    def get(self,request,*args,**kwargs):
        category = request.GET.get('category')
        if category == 'all':
            socials = Social.objects.all().order_by('-date_added')
        elif category is None:
            socials = Social.objects.all().order_by('-date_added')            
            
        else:
            socials = Social.objects.filter(category=category).order_by('-date_added')
        return Response({
            'socials':SocialSerializer(socials,many=True).data
        })
    def post(self,request,*args,**kwargs):
        post_type=request.data.get('post_type')

        serializer=SocialSerializer(data=request.data)
        if serializer.is_valid():
            serializer=serializer.save(
                user=request.user
            )
            

            serialized_data=SocialSerializer(serializer,many=False).data

            return Response(serialized_data)

        else:
            return Response({'invalid':True,'data':request.data})

class SocialDetailUpdateView(RetrieveUpdateAPIView):
    queryset=Social.objects.all()
    serializer_class=SocialSerializer
    authentication_classes =[TokenAuthentication,]

    # def get(self,request,pk,*args,**kwargs):
    #     # response=super().retrieve(request,pk,*args,**kwargs)
    #     post=Social.objects.get(id=pk)
    #     likes_count=LikeUnlikeSerializer(post.likes.all().count(),many=False).data

    #     return Response(
    #         likes_count
    #     )


        

class CategoryView(APIView):
    def get(self,request,post_type,*args,**kwargs):

        try:

            # post_type=request.GET.get('post_type').lower()
            category=PostType.objects.get(type__iexact=post_type)
            post=category.categories
            # post=Social.objects.filter(category__type=post_type)

            return Response({
                'category':SocialSerializer(post,many=True).data
                # 'category':PostTypeSerializer(category,many=False).data
            })
        except ObjectDoesNotExist:
            return Response('no content found')



class LikeUnlikeView(APIView):
    authentication_classes =[TokenAuthentication,]
    def get(self,request,id):
        # post_id=str(request.data['post_id'])

        
        post=Social.objects.get(id=id)
        liked=False
        if request.user not in post.likes.all():
            post.likes.add(request.user)
            liked=True

            return Response({
                'status':'post liked',
                'liked': True
            })
        

        else:
            post.likes.remove(request.user)
            liked=False
            return Response({
                'status':'post unliked',
                'liked': False
            })



class CommentView(APIView):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    authentication_classes =[TokenAuthentication,]

    def post(self,request,id,*args,**kwargs):
        post=Social.objects.get(id=id)
        serializer=CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer=serializer.save(
                user=request.user,
                post=post
            )

            serialized_data=CommentSerializer(serializer, many=False).data

            return Response({
                'status':'sent',
                'comment':serialized_data
            })
        else:
            return Response({
                'status':'failed'
            })
            
    def get(self,request,id,*args,**kwargs):
        post=Social.objects.get(id=id)
        filters=getfilters(request,exclude=[''],contain_words=['',])
        comments=Comment.objects.filter(post=post,**filters)

        return Response({
            'comments':CommentSerializer(comments,many=True).data
        })


# class MapView(APIView):

#     def get(self,request):
#         return Response({
#             'maps':MapSerializer(Maps.objects.filter(user=request.user),many=True).data
#         })
#     def post(self,request):
#         serializer=MapSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer=serializer.save(
#                 user=request.user
#             )
#             serialized_data=MapSerializer(serializer).data

#             return Response(serialized_data)
