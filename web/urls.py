from django.urls import path, re_path
from . import views

urlpatterns = [

    re_path(r'^$', views.IndexView.as_view(), name='web.index'),
    re_path(r'^login$', views.LoginView.as_view(), name='web.login'),
    re_path(r'^logout$', views.LogoutView.as_view(), name='web.logout'),
]
