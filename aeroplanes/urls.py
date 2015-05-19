from django.conf.urls import url
import views
__author__ = 'Lee.Gent'

urlpatterns = [
    url(r'^(?P<aeroplane_id>\d+)$', views.aeroplane, name="aeroplane"),
]
