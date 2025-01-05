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
    content = models.TextField(verbose_name='Message Content',null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name}: {self.content[:20]} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
