from rest_framework.serializers import ModelSerializer
from .models import UserPost, PostMedia, PostLikes
from users.serializers import UserProfileViewSerializer
from users.models import UserProfile
from rest_framework import serializers

class UserPostCreateSerializer(ModelSerializer):

    def create(self, validated_data):

        validated_data['author'] = self.context['current_user']

        return UserPost.objects.create(**validated_data)

    class Meta :
        model = UserPost
        fields = ('caption_text', 'location', 'id', 'is_published', )


class PostMediaCreateSerializer(ModelSerializer):


    class Meta :
        model = PostMedia
        fields = ('media_file', 'sequence_index', 'post')


class PostMediaViewSerializer(ModelSerializer):

    class Meta :
        model = PostMedia
        exclude = ('post', )
        # fields = '__all__'

class PostFeedSerializer(ModelSerializer):

    author = UserProfileViewSerializer()
    media = PostMediaViewSerializer(many=True, source='content')


    class Meta : 
        model = UserPost
        fields = '__all__'
        include = ('author', 'media', )

class PostLikeCreateSerializer(ModelSerializer):

    def create(self, validated_data):
        validated_data['liked_by'] = self.context['current_user']
        
        return PostLikes.objects.create(**validated_data)

    class Meta:
        model = PostLikes
        fields = ('id', 'post', )

class PostLikesViewSerializer(ModelSerializer):

    liked_by = serializers.SerializerMethodField()
    post = UserPostCreateSerializer()

    def get_liked_by(self, obj):
        return {'id':obj.liked_by.user.id,
                'username': obj.liked_by.user.username}

    class Meta:
        model = PostLikes
        fields = ('post','liked_by', )
