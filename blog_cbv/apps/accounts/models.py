from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models

from apps.services.utils import unique_slugify


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    slug=models.SlugField(verbose_name="URL",max_length=255,blank=True)
    avatar=models.ImageField(
        verbose_name='Фотография профиля',
        upload_to='images/avatars/%Y/%m/%d/',
        default='images/avatars/default.jpg',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        blank=True,
    )
    bio=models.TextField(verbose_name='Биография',blank=True,max_length=500)
    birth_day=models.DateField(verbose_name='Дата рождения',blank=True,null=True)


    class Meta:
        verbose_name='Профиль'
        verbose_name_plural='Профили'
        ordering=['user']


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=unique_slugify(self,self.user.username,self.slug)
        super(Profile,self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('accounts:profile_detail',kwargs={'slug':self.slug})