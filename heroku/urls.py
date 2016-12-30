# -*- coding: UTF-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^', include('symcon.urls')),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
urlpatterns += staticfiles_urlpatterns()
