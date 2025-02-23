"""
URL configuration for mysite project.

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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import accounts.urls
import blog.urls
from django.contrib.sitemaps.views import sitemap

import blog_api.urls
from blog.sitemaps import PostSitemap
from mysite import settings

sitemaps = {
    'sites': PostSitemap,
}
urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include(blog.urls, namespace='blog')),
    path('accounts/', include(accounts.urls, namespace='accounts')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('auth/', include('social_django.urls', namespace='social')),
    path('api/', include(blog_api.urls)),
    path("api-auth/", include("rest_framework.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
