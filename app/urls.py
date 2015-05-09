from django.conf.urls import patterns, url

from app import views, views_datasets, views_contributors

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
  url(r'^accounts/profile/$', views.accounts_profile, name='accounts_profile'),
  url(r'^users/search/(?P<query>\w+)/$', views_contributors.search, name='contributors_search'),

  # Datasets
  url(r'^datasets/new/$', views_datasets.new, name='datasets_new'),
  url(r'^datasets/(?P<dataset_id>[0-9]+)/$', views_datasets.show, name='datasets_show'),
  url(r'^datasets/(?P<dataset_id>[0-9]+)/download/$', views_datasets.download, name='datasets_download'),
  url(r'^datasets/(?P<dataset_id>[0-9]+)/contributors/$', views_contributors.create, name='contributors_create'),
  url(r'^datasets/(?P<dataset_id>[0-9]+)/contributors/(?P<contributor>\w+)/$', views_contributors.destroy, name='contributors_destroy'),

)
