from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from mptt.models import TreeForeignKey, MPTTModel
from django.shortcuts import reverse
from taggit.managers import TaggableManager

from apps.services.utils import unique_slugify


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('author', 'category').filter(status='PB')


class Post(models.Model):
    STATUS_CHOICES = (
        ('DF', 'Черновик'),
        ('PB', 'Опубликовано')
    )
    title = models.CharField(verbose_name='Название записи', max_length=255)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True)
    description = models.TextField(max_length=500, verbose_name='Краткоe описание')
    text = models.TextField(verbose_name='Полный текст записи')
    trumbnail = models.ImageField(
        default='images/thumbnails/site.png',
        upload_to='images/thumbnails/%Y/%m/%d/',
        blank=True,
        verbose_name='Фотографии поста',
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'webp', 'jpeg', 'gif'])]
    )
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=2,
        default='PB',
        verbose_name='Статус')
    create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    author = models.ForeignKey(User,
                               on_delete=models.SET_DEFAULT,
                               default=1,
                               related_name='author_posts',
                               verbose_name='Автор поста')
    updater = models.ForeignKey(User,
                                on_delete=models.SET_NULL,
                                blank=True,
                                null=True,  # отсутствие связи с пользователем в бд
                                related_name='updater_posts',
                                verbose_name='Обновил')
    fixed = models.BooleanField(default=False, verbose_name='Прикреплено')
    category = TreeForeignKey('Category',
                              on_delete=models.PROTECT,
                              related_name='posts',
                              verbose_name='Категория')
    objects = models.Manager()  # указываем если есть кастом мэнеджер
    custom = PostManager()
    tags=TaggableManager()

    class Meta:
        db_table = 'blog_post'
        ordering = ['-create', '-fixed']
        indexes = [models.Index(fields=['-create', '-fixed', 'status'])]
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return f'{self.title} by {self.author}'

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        """
        При сохранении генерируем слаг и проверяем на уникальность
        """
        self.slug = unique_slugify(self, self.title, self.slug)
        super(Post, self).save(*args, **kwargs)


class Category(MPTTModel):
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(blank=True, unique=True, verbose_name='URL', max_length=255)
    description = models.CharField(max_length=300, verbose_name='Описание категории')
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True,
        db_index=True,
        verbose_name='Родительская категория'
    )

    class MPTTMeta:
        order_insertion_by = ['title']  # сортировка по вложенности

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'blog_category'

    def get_absolute_url(self):
        return reverse('blog:post_by_category', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Comment(MPTTModel):
    STATUS_CHOICES = (
        ('PB', 'Опубликовано'),
        ('DF', 'Черновик'),
    )
    post = models.ForeignKey(
        Post,
        verbose_name='Пост',
        related_name='comments',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments_author',
        verbose_name='Автор'
    )
    content = models.CharField(max_length=3000, verbose_name='Текст комментария')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(verbose_name='Время обновления', auto_now=True)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=2,
        default='PB',
        verbose_name='Статус комментария'
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True,
        verbose_name='Родительский комментарий'
    )

    class MPTTMeta:
        order_insertion_by = ['time_create']

    class Meta:
        ordering = ['-time_create']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author}:{self.content[:50]}...' if len(self.content) > 50 else f'{self.author}:{self.content}'
