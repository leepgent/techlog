from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.group, name="group"),
    url(r'^create/$', views.creategroup, name="creategroup"),
    url(r'^join/(?P<secret>[\w\d-]+)/$', views.join_group, name="joingroup"),

]
