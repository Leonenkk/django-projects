from django.contrib import admin

from blog.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=('title','slug','author','status','published')  #поля отображаемые на странице всех объектов
    list_filter=('status','published','created','author')  #панель слева с полями для фильтрации
    search_fields=('title','body','published')#поиск
    date_hierarchy='published'  #под поиском строка с хронологией по датам
    ordering=('published','status') #сортировка на стр объектов
    prepopulated_fields={'slug':('title',) }#словарь для автозаполнения 1-что копировать : (2)-куда
    raw_id_fields=('author',)  #добавление поиска, но только для связанных полей с др моделью

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('post','name','email','created','active')
    list_filter=('created','active','updated')
    search_fields=('name','email','body')
    date_hierarchy='created'


