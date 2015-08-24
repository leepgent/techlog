from django.conf.urls import url, include
import views
from log import urls as techlog_urls
__author__ = 'Lee.Gent'

urlpatterns = [
    url(r'^(?P<aeroplane_reg>[\w\d-]+)/$', views.aeroplane, name="aeroplane"),
    url(r'^(?P<aeroplane_reg>[\w\d-]+)/consumables$', views.consumables, name="consumables"),
    url(r'^(?P<aeroplane_reg>[\w\d-]+)/log/', include(techlog_urls)),
]
