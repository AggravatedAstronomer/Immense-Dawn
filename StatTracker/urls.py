from django.conf.urls import url
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^summoner/$', views.detail, name='detail'),
    #url(r'^summoner/(?P<summoner_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^name/$', views.search_summoner, name='search_summoner'),
    url(r'^harvested/(?P<task_id>.*)/$', views.harvested, name='harvested'),
    url(r'^is_complete/(?P<task_id>.*)/$', views.is_complete, name='is_complete'),
    url(r'^riot\.txt$', TemplateView.as_view(template_name='StatTracker/riot.txt', content_type="text/plain")),
]
