from rest_framework.serializers import ModelSerializer
from .models import UserPost, PostMedia
from users.serializers import UserProfileViewSerializer



class UserPostCreateSerializser(ModelSerializer):

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
    # print('this is line 29-------------------->')

    class Meta :
        model = PostMedia
        # exclude = ('post', )
        fields = '__all__'

class PostFeedSerializer(ModelSerializer):

    author = UserProfileViewSerializer()
    media = PostMediaViewSerializer(many=True, read_only=True, source='content')


    class Meta : 
        model = UserPost
        fields = ('caption_text', 'location', 'is_published', 'media', 'author', )
        # include = ('media', )
        

