from django.conf.urls import url
from django.contrib.auth.decorators import login_required
import views
__author__ = 'Lee.Gent'

urlpatterns = [
    url(r'^$', views.log_entries_redirect, name='techlogentrylist'),
    url(r'^(?P<year>\d+)/(?P<month>\d+)$', views.log_entries, name="techlogentrylist_by_date"),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/technical$', views.log_entries_technical, name="techlogentrylist_technical"),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/technical/print$', views.log_entries_technical_print, name="techlogentrylist_technical_print"),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/xml$', views.log_entries_xml, name="techlogentrylist_by_date_xml"),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/json$', views.log_entries_json, name="techlogentrylist_by_date_json"),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/monthsummary$', views.month_summary, name="log_month_summary"),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/cap398$', views.cap398, name="cap398_by_date"),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/cap398/print$', views.cap398_print, name="cap398_by_date_print"),
    url(r'^add$', views.add_flight, name='addflight'),
    url(r'^(?P<pk>\d+)/$', views.view_entry, name="logentry"),
    url(r'^delete/(?P<pk>\d+)/$', views.delete_logentry, name="delete_logentry"),
]
