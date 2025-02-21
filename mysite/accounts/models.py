from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar=models.ImageField(default='default.png',upload_to='profile_images')
    biography=models.TextField(blank=True,null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img=Image.open(self.avatar.path)
        if img.height>100 or img.width>100:
            new_size=(100,100)
            img.thumbnail(new_size)
            img.save(self.avatar.path)


    def __str__(self):
        return f'Profile for user: {self.user.username}'

