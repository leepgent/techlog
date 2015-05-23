from django.conf.urls import url
import views

urlpatterns = [
    url(r'^join/$', views.join, name="join"),
]
