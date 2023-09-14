from django.shortcuts import render
from users.models import User, UserProfile, NetworkEdge
from .form import UserSignUpForm
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserCreateSerializer, UserProfileViewSerializer, UserProfileUpdateSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework import mixins, generics
from .serializers import NetworkEdgeCreatonSerializer, NetworkEdgeFollowingSerializer, NetworkEdgeFollowersSerializer
# Create your views here.

def index(request):

    count_of_users = User.objects.count()
    users = User.objects.all()

    for user in users:
        print(user.username)

    context = {
        "count_of_users": count_of_users,
        "users": users
    }

    return render(request, 'users/index.html', context)

def signup(request):

    form = UserSignUpForm()
    errors = []
    message = None

    if request.method == "POST":

        form = UserSignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            message = "New user created"
        else:
            errors = form.errors

    context = {
        'form': form,
        'errors': errors,
        'message': message

    }

    return render(request, 'users/signup.html', context)

@api_view(['POST'])
def CreateUser(request):

    serializer = UserCreateSerializer(data=request.data)

    response_data = {
        
    }

    if serializer.is_valid():
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        response_data['data'] = { 
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        response_status = status.HTTP_201_CREATED
    else :
        response_data['errors'] = serializer.errors
        response_status = status.HTTP_204_NO_CONTENT
        

    return Response(response_data, response_status)
    

class UserProfileDetail(generics.GenericAPIView, mixins.DestroyModelMixin,
                        mixins.RetrieveModelMixin, mixins.UpdateModelMixin):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileViewSerializer

    queryset = UserProfile.objects.all()

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if self.request.method == 'DELETE':
            return User.objects.all().filter(pk=pk)
        return self.queryset.filter(pk=pk)
    
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UserProfileUpdateSerializer
        return self.serializer_class

    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        pk=self.kwargs.get('pk')
        if request.user.id !=pk:
            return Response(f"{request.user.username} it's not your profile you are tyring to upload", status=status.HTTP_204_NO_CONTENT)
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if request.user.id !=pk:
            message = f"{request.user} you don't have permissions to delete another user."
            return Response(message, status=status.HTTP_204_NO_CONTENT)
        return self.destroy(request, *args, **kwargs)
    
class UserList(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        users = UserProfile.objects.all()

        serialized_data = UserProfileViewSerializer(instance=users, many= True)

        return Response(serialized_data.data, status=status.HTTP_200_OK)
    

class UserNetworkEdgeView(mixins.CreateModelMixin, mixins.ListModelMixin,
                          generics.GenericAPIView):

    queryset = NetworkEdge.objects.all()
    serializer_class = NetworkEdgeCreatonSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get_serializer_class(self):

        if self.request.method == 'GET':
            if self.request.query_params['direction']=='following':
                return NetworkEdgeFollowingSerializer
            return NetworkEdgeFollowersSerializer
            return NetworkEdgeViewSerializer
        
        return self.serializer_class
    

    def get_queryset(self):

        edge_direction = self.request.query_params['direction']

        if edge_direction == 'followers':
            # NetworkEdge.objects.all().filter(to_user = self.request.user.profile)
            return self.queryset.filter(to_user = self.request.user.profile)
        
        elif edge_direction == 'following':
            return self.queryset.filter(from_user = self.request.user.profile)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        request.data['from_user'] = request.user.profile.id

        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):

        network_edge = NetworkEdge.objects.filter(from_user = request.user.profile,
                                                  to_user = request.data['to_user'])
                                                          
        if network_edge.exists():
            network_edge.delete()
            message = f'user {User.objects.get(id=request.data["to_user"])} unfollowed successfully'
        else:
            message = 'no edge found'

        return Response({'data':None, 'message':message}, status=status.HTTP_200_OK)
        
        return self.destroy(request, *args, **kwargs)