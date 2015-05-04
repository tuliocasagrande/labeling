from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
  url(r'^datasets/new$', views.datasets_new, name='datasets_new'),
  url(r'^datasets/(?P<datasets_id>[0-9]+)$', views.datasets_show, name='datasets_show'),
  url(r'^accounts/profile/$', views.accounts_profile, name='accounts_profile'),
)
