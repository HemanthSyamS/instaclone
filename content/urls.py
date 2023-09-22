from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'like', views.PostLikeViewSet, basename='likes')
router.register('comments', views.PostCommentsViewSet)


urlpatterns = [
    path('', views.UserPostCreateFeed.as_view(), name = 'user_post_view'),
    path('media/', views.PostMediaView.as_view(), name = 'post_media_view'),
    path('<int:pk>/', views.UserPostDetailUpdateView.as_view(), name = 'post_detail_update'),
    path('', include(router.urls))
]