from django.conf.urls import url
from django.contrib.auth.decorators import login_required
import views
__author__ = 'Lee.Gent'

urlpatterns = [
    url(r'^$', login_required(views.LogEntryList.as_view()), name='techlogentrylist'),
    url(r'^add$', views.add_flight, name='addflight'),
    url(r'^(?P<pk>\d+)/$', views.view_entry, name="logentry"),
    url(r'^delete/(?P<pk>\d+)/$', views.delete_logentry, name="delete_logentry"),
]
