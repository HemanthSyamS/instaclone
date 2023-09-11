from django.shortcuts import render
from .models import UserPost
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from .serializers import UserPostCreateSerializser, PostMediaCreateSerializer, PostFeedSerializer, PostMediaViewSerializer
from rest_framework import mixins
from .filters import CurrentUserFollowingFilterBackend
from rest_framework.response import Response
from rest_framework import status


# Create your views here.


class UserPostCreateFeed(mixins.CreateModelMixin,mixins.ListModelMixin,
                         generics.GenericAPIView ):

    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication]

    queryset = UserPost.objects.all()
    serializer_class = UserPostCreateSerializser
    filter_backends = [CurrentUserFollowingFilterBackend]

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


class UserPostDetailUpdateView(mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                               mixins.DestroyModelMixin, generics.GenericAPIView):
    
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication]

    serializer_class = UserPostCreateSerializser
    queryset = UserPost.objects.all()
    # print('line 44----------->',queryset)

    def get_serializer_class(self):

        if self.request.method == 'GET':
            return PostFeedSerializer

        return self.serializer_class

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.is_published:
            
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
         
        return Response("There are no published posts from users your follow")


    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, pk):
        # print(f'user post {request.id}', request.user.profile.post.filter(id=pk))
        # print(f'post deleted by {request.user.username}')
        return Response({'data':None, 'message':'post deleted by user'}, status=status.HTTP_200_OK)

        return self.destroy(request, pk,response_data="success")