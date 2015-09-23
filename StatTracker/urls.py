from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^summoner/$', views.detail, name='detail'),
    #url(r'^summoner/(?P<summoner_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^name/$', views.search_summoner, name='search_summoner'),
]
