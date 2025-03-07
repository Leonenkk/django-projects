from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.blog.models import Post, Category, Comment, Rating
from django_mptt_admin.admin import DjangoMpttAdmin


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['preview']

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.trumbnail.url}" width="150"/>')


@admin.register(Comment)
class CommentAdmin(DjangoMpttAdmin):
    pass

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass
