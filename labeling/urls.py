from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
  url(r'^admin/', include(admin.site.urls)),
  url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
  url(r'^accounts/', include('allauth.urls')),
  url(r'^', include('app.urls')),
]
