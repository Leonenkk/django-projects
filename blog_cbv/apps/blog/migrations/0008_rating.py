# Generated by Django 5.1.6 on 2025-03-07 17:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_post_description_alter_post_text'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(choices=[(1, 'Нравится'), (-1, 'Не нравится')], verbose_name='Количество')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время оценки поста')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP адрес')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='blog.post', verbose_name='Запись')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_ratings', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Рейтинг',
                'verbose_name_plural': 'Рейтинги',
                'ordering': ['-time_create'],
                'indexes': [models.Index(fields=['-time_create', 'value'], name='blog_rating_time_cr_95b965_idx')],
                'unique_together': {('ip_address', 'post')},
            },
        ),
    ]
