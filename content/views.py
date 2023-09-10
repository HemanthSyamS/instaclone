from django.shortcuts import render
from .models import UserPost
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from .serializers import UserPostCreateSerializser, PostMediaCreateSerializer, PostFeedSerializer, PostMediaViewSerializer
from rest_framework import mixins
# Create your views here.


class UserPostCreateFeed(mixins.CreateModelMixin,mixins.ListModelMixin,
                         generics.GenericAPIView ):

    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication]

    queryset = UserPost.objects.all()
    serializer_class = UserPostCreateSerializser

    def get_serializer_context(self):
        return {'current_user' : self.request.user.profile}

    def get_serializer_class(self):
        
        if self.request.method == 'GET':
            return PostFeedSerializer

        return self.serializer_class

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PostMediaView(mixins.CreateModelMixin, generics.GenericAPIView):
    
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication]

    serializer_class = PostMediaCreateSerializer

    def put(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserPostDetailUpdateView(mixins.UpdateModelMixin, generics.GenericAPIView):
    
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication]

    serializer_class = UserPostCreateSerializser
    queryset = UserPost.objects.all()
    # print('line 44----------->',queryset)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)