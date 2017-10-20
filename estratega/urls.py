"""estratega URL Configuration

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
from django.contrib.auth import views as auth_views

from estrategias import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^quees', views.quees, name='quees'),
    url(r'^login', views.EstrategaLoginView.as_view(), name='login'),
    url(r'^logout', views.log_out, name='logout'),
    url(r'^error_inesperado', views.error_inesperado, name='error_inesperado'),
    url(r'^metodologia', views.metodologia, name='metodologia'),
    url(r'^estrategias/', include('estrategias.urls', namespace='estrategias')),
    url(r'^admin/', include(admin.site.urls)),
]
