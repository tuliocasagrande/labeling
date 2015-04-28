from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
  url(r'^new_dataset$', views.new_dataset, name='new_dataset'),
)
