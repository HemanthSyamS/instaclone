from django.shortcuts import render
from users.models import User,   UserProfile
from .form import UserSignUpForm
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserCreateSerializer, UserProfileViewSerializer, UserProfileUpdateSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

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

    # print('On line 54',request.data)
    serializer = UserCreateSerializer(data=request.data)

    response_data = {
        "data": None,
        "errors" : None
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

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def UserList(request):
    # print('On line 87 -->', request.user)
    users = UserProfile.objects.all()

    serialized_data = UserProfileViewSerializer(instance=users, many= True)

    return Response(serialized_data.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def GetUser(request, pk=None):
    user = UserProfile.objects.filter(id=pk).first()

    if user:
        serializer = UserProfileViewSerializer(instance=user, many=False)
        response_data = {
            'data': serializer.data,
            'errors': None
        }
        response_status= status.HTTP_200_OK
    else : 
        response_data = {
            'data': None,
            'errors': "User does not exist!"
        }
        response_status = status.HTTP_404_NOT_FOUND

    return Response(data=response_data, status=response_status)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def UpdateUserProfile(request):

    user_profile_serializer = UserProfileUpdateSerializer(instance=request.user.profile,
                                                              data=request.data)
    # print(user_profile_serializer)
    response_data = {
        "data": None,
        "errors": None
    }

    if user_profile_serializer.is_valid():
        user_profile = user_profile_serializer.save()

        response_data['data'] = UserProfileViewSerializer(instance=user_profile).data
        # print(response_data)

        response_status = status.HTTP_200_OK

    else:

        response_data['errors'] = user_profile_serializer.errors
        response_status = status.HTTP_400_BAD_REQUEST

    return Response(response_data, status=response_status)