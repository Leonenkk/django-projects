from django.contrib import admin
from apps.blog.models import Post,Category
from django_mptt_admin.admin import DjangoMpttAdmin


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}