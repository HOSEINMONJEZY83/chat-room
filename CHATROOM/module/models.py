from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.


class User(AbstractUser):
    avatar = models.ImageField(upload_to='image',verbose_name='profile',null=True,blank=True)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        if self.username is not '':
            return self.username
        return self.email

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='Message Content', null=True, blank=True)
    image = models.ImageField(upload_to='pic', null=True, blank=True)
    audio = models.FileField(upload_to='audio', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.content:
            preview = self.content[:20]
        elif self.image:
            preview = "Image"
        elif self.audio:
            preview = "Audio"
        else:
            preview = "Empty"
        return f"{self.user.first_name}: {preview} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

