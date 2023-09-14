from django.urls import path
from . import views


urlpatterns = [
    path('', views.UserPostCreateFeed.as_view(), name = 'user_post_view'),
    path('media/', views.PostMediaView.as_view(), name = 'post_media_view'),
    path('<int:pk>/', views.UserPostDetailUpdateView.as_view(), name = 'post_detail_update')
]