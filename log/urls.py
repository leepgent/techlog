from django.conf.urls import url
import views
__author__ = 'Lee.Gent'

urlpatterns = [
    url(r'^$', views.LogEntryList.as_view(), name='techlogentrylist'),
    url(r'^(?P<pk>\d+)/$', views.LogEntryDetailView.as_view(), name="logentry"),
]
