from django.conf.urls import url
import views
__author__ = 'Lee.Gent'

urlpatterns = [
    url(r'^$', views.LogEntryList.as_view(), name='techlogentrylist'),
    url(r'^(?P<logentry_id>\d+)$', views.logentry, name="logentry"),
]
