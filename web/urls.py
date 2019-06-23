from django.urls import path, re_path
from . import views

urlpatterns = [

    re_path(r'^$', views.IndexView.as_view(), name='web.index'),
    re_path(r'^login$', views.LoginView.as_view(), name='web.login'),
    re_path(r'^logout$', views.LogoutView.as_view(), name='web.logout'),

    # path("index/", views.index, name="webapp.index"),
    # re_path(r'^(?P<pod_name>[^/]+)/$', views.pod_log, name='webapp.pod_log'),
    # re_path(r'^create/(?P<yaml_url>[^/]+)/$', views.submit_yaml_by_url, name='webapp.submit_yaml_by_url'),
]
