"""
URL configuration for blog_cbv project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from blog_cbv import settings
from django.conf.urls.static import static
import apps.blog.urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.blog.urls',namespace='blog')),
    path('',include('apps.accounts.urls',namespace='accounts')),
    path('ckeditor5/',include('django_ckeditor_5.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path('__debug__/', include('debug_toolbar.urls')),
    #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
