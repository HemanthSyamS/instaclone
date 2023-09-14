from django.db import models
from django.contrib.auth.models import User

# class User(models.Model):

#     name = models.CharField(max_length=255, null=False)
#     email = models.CharField(max_length=255, unique=True, null=False)
#     phone_number = models.CharField(max_length=10, unique=True)
#     password = models.CharField(max_length=55, null=False)
#     is_active = models.BooleanField(default=False)

#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)

class TimeStamp(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(models.Model):

    def media_name(instance, filename):
        ext = filename.split('.')[-1]

        return f'profile_pic/{instance.user.id}_{instance.user.username}.{ext}'

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False,
                                related_name = 'profile')
    profile_pic_url = models.ImageField(upload_to= media_name, blank=True)
    bio = models.CharField(max_length=255, blank=True)
    is_verified = models.BooleanField(default=True)


class NetworkEdge(models.Model):

    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                  related_name='following')
    
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, 
                                related_name= 'followers')
    
    class Meta:
        unique_together = ('from_user', 'to_user', )
    