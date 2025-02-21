from django.urls import path
from logic.views import index, create, delete,edit

app_name='crud'
urlpatterns=[
    path('', index, name='index'),
    path('create/',create, name='create'),
    path('delete/<int:person_id>/',delete, name='delete'),
    path('edit/<int:person_id>/',edit, name='edit'),
]