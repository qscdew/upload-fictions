"""book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from homepage import views
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.index,name='index'),
    url(r'^books/(?P<book_id>\d+)/$',views.book,name='book'),
    url(r'^writers/(?P<writer_id>\d+)/$',views.writer,name='writer'),
    url(r'^newbook/', views.newbook,name='newbook'),
    url(r'^xz/(?P<book_name>\S+)/$',views.file_down,name='down'),
    url(r'^newwriter/', views.newwriter,name='newwriter'),
    url(r'^users/', include('users.urls', namespace='users')), 
    url(r'^favicon\.ico$', favicon_view),
    url(r'^bbs/', views.newliuyan,name='liuyan'),
    
    url(r'^v/(?P<video_name>\S+)/$',views.video,name='v'),
    

    
    
]
