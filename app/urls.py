from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
  url(r'^dataset/new$', views.dataset_new, name='dataset_new'),
  url(r'^accounts/profile/$', views.account_profile, name='account_profile'),
)
