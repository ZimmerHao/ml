from django.urls import path, re_path
from . import views

urlpatterns = [
    path("index/", views.index, name="webapp.index"),
    re_path(r'^(?P<pod_name>[^/]+)/$', views.pog_log, name='webapp.pod_log'),
]
