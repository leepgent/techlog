from django.conf.urls import url
from django.contrib.auth.decorators import login_required
import views
__author__ = 'Lee.Gent'

urlpatterns = [
    url(r'^$', views.log_entries, name='techlogentrylist'),
    url(r'^(?P<year>\d+)/(?P<month>\d+)$', views.log_entries),
    url(r'^add$', views.add_flight, name='addflight'),
    url(r'^(?P<pk>\d+)/$', views.view_entry, name="logentry"),
    url(r'^delete/(?P<pk>\d+)/$', views.delete_logentry, name="delete_logentry"),
]
