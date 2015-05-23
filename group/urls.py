from django.conf.urls import url
import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.group, name="group"),
    url(r'^join/(?P<secret>[\w\d-]+)/$', views.joingroup, name="joingroup"),

]
