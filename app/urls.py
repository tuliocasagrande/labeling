from django.conf.urls import patterns, url

from app import views, views_datasets, views_contributors

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^accounts/profile/$',
        views.accounts_profile, name='accounts_profile'),
    url(r'^users/search/(?P<query>\w+)/$',
        views_contributors.search, name='contributors_search'),

    # Datasets
    url(r'^datasets/new/$',
        views_datasets.new, name='datasets_new'),
    url(r'^datasets/create/$',
        views_datasets.create, name='datasets_create'),
    url(r'^datasets/(?P<dataset_id>[0-9]+)/$',
        views_datasets.show, name='datasets_show'),
    url(r'^datasets/(?P<dataset_id>[0-9]+)/edit/$',
        views_datasets.edit, name='datasets_edit'),
    url(r'^datasets/(?P<dataset_id>[0-9]+)/update/$',
        views_datasets.update, name='datasets_update'),
    url(r'^datasets/(?P<dataset_id>[0-9]+)/destroy/$',
        views_datasets.destroy, name='datasets_destroy'),
    url(r'^datasets/(?P<dataset_id>[0-9]+)/label/$',
        views_datasets.label, name='datasets_label'),
    url(r'^datasets/(?P<dataset_id>[0-9]+)/download/$',
        views_datasets.download, name='datasets_download'),

    # Contributors
    url(r'^datasets/(?P<dataset_id>[0-9]+)/contributors/$',
        views_contributors.create, name='contributors_create'),
    url(r'^datasets/(?P<dataset_id>[0-9]+)/contributors/(?P<contributor>\w+)/$',
        views_contributors.destroy, name='contributors_destroy'),

)
