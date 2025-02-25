from django.contrib.auth.models import User
from accounts.models import Profile
from django.db.models.signals import post_save # исп когда объект модели сохранен в бд, в данном случае юзер
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

'''
Сигналы  позволяют выполнять дополнительные действия в ответ на изменения в моделях.
'''


@receiver(post_save, sender=User)# вызывается всегда когда создается или обновл юзер
def create_profile(sender, instance, created,**kwargs):#sender-модель отпр сигнал, instance-экзмпляр модели,который был сохр
    if created: #created-булевое, True-если объект создался
        Profile.objects.create(user=instance)
        Token.objects.create(user=instance)