from . import views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenObtainPairView



urlpatterns  = [
    path('index/', views.index, name = 'users_main_view'),
    path('signup/', views.signup, name= 'users_signup'),

    path('add/', views.CreateUser, name = 'create_user_api'),
    # path('token/refresh', TokenRefreshView.as_view(), name = 'refresh_token_api')
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('login/', TokenObtainPairView.as_view(), name='login_api'),

    path('list/', views.UserList.as_view(), name = 'user_list'),

    path('<int:pk>/', views.UserProfileDetail.as_view(), name = 'modify_user'),




]