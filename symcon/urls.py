# -*- coding: UTF-8 -*-
from django.conf.urls import url

from symcon import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='symcon_index'),
    url(r'^page/(?P<page>\d+)$', views.IndexView.as_view(), name='symcon_index_page'),
    url(r'^library/submit$', views.LibrarySubmitView.as_view(),
        name='symcon_library_submit'),
    url(r'^library/(?P<library_id>[^/]+)$', views.LibraryView.as_view(), name='symcon_library'),
    url(r'^library/(?P<library_id>[^/]+)/module/(?P<module_id>[^/]+)$',
        views.LibraryModuleView.as_view(), name='symcon_library_module'),
]
