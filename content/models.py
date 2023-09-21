from django.db import models
from users.models import TimeStamp, UserProfile
# Create your models here.

class UserPost(TimeStamp):

    caption_text = models.CharField(max_length=255, null=True)
    location = models.CharField(null=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name= 'posts')

    is_published = models.BooleanField(default=False)


class PostMedia(TimeStamp):

    def media_name(instance, filename):
        ext = filename.split('.')[-1]

        return f'post_media/{instance.post.id}_{instance.sequence_index}.{ext}'
    
    media_file = models.FileField(upload_to=media_name)
    sequence_index = models.PositiveSmallIntegerField(default=0)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='content')

    class Meta:

        unique_together = ('sequence_index', 'post', )


class PostLikes(TimeStamp):

    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name= 'likes')
    liked_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name= 'liked_posts')

    class Meta:
        unique_together = ('post', 'liked_by', )

class PostComments(TimeStamp):

    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name= 'comments')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name= 'comments_made')
    text = models.CharField(max_length=255)
