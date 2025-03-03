from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.accounts.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','slug','birth_day']
    list_display_links = ['user','slug']

    def preview_avatar_image(self, obj):
        return mark_safe(f'<img src="{obj.avatar.url}"width="150"/>')
