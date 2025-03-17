from django.core.cache import cache
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models

from apps.services.utils import unique_slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(verbose_name="URL", max_length=255, blank=True)
    avatar = models.ImageField(
        verbose_name='Фотография профиля',
        upload_to='images/avatars/%Y/%m/%d/',
        default='images/avatars/default.jpg',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        blank=True,
    )
    bio = models.TextField(verbose_name='Биография', blank=True, max_length=500)
    birth_day = models.DateField(verbose_name='Дата рождения', blank=True, null=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['user']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.user.username, self.slug)
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('accounts:profile_detail', kwargs={'slug': self.slug})

    def is_online(self):
        cache_key = f'last-seen-{self.user.id}'
        last_seen = cache.get(cache_key)

        if last_seen is not None:
            return True
        return False



class Project(models.Model):
    name=models.CharField(verbose_name="Название проекта",help_text="Введите название проекта",max_length=200)
    start_date=models.DateField(verbose_name="Дата начала проекта",help_text="Укажите дату начала проекта")
    end_date=models.DateField(verbose_name="Дата окончания проекта",help_text="Укажите дату окончания проекта")
    budget=models.DecimalField(verbose_name="Бюджет проекта",help_text="Введите бюджет проекта",max_digits=12,decimal_places=2)
    progress=models.PositiveSmallIntegerField(verbose_name="Процент выполнения",help_text="Введите процент выполнения проекта")
    description=models.TextField(verbose_name="Описание проекта",help_text="Введите описание проекта")
    is_completed=models.BooleanField(verbose_name="Проект завершён",help_text="Укажите, завершён ли проект",default=False)
    repository_url=models.URLField(verbose_name="URL репозитория",help_text="Введите URL репозитория проекта")
    manager=models.CharField(verbose_name="Менеджер проекта",help_text="Введите имя менеджера проекта",max_length=50)
    slug=models.SlugField(verbose_name="Слаг проекта",help_text="Введите слаг проекта",max_length=255,unique=True)

