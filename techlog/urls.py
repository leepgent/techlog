"""logbook URL Configuration

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
from dashboard import views
from group import urls as group_urls
from aeroplanes import urls as aeroplanes_urls
from registration import urls as registration_urls

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^registration/', include(registration_urls)),
    url(r'^dashboard', views.dashboard),
    url(r'^groups/', include(group_urls)),
    url(r'^aeroplanes/', include(aeroplanes_urls)),
    url(r'^admin/', include(admin.site.urls)),
]
