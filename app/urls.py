from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
  url(r'^accounts/profile/$', views.accounts_profile, name='accounts_profile'),
  url(r'^users/search/(?P<query>\w+)/$', views.contributors_search, name='contributors_search'),

  # Datasets
  url(r'^datasets/new/$', views.datasets_new, name='datasets_new'),
  url(r'^datasets/(?P<dataset_id>[0-9]+)/$', views.datasets_show, name='datasets_show'),
  url(r'^datasets/(?P<dataset_id>[0-9]+)/download/$', views.datasets_download, name='datasets_download'),
  url(r'^datasets/(?P<dataset_id>[0-9]+)/contributors/$', views.contributors_create, name='contributors_create'),
  url(r'^datasets/(?P<dataset_id>[0-9]+)/contributors/(?P<contributor>\w+)/$', views.contributors_destroy, name='contributors_destroy'),

)
