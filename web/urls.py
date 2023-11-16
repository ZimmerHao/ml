from django.urls import path, re_path, include
from . import views

urlpatterns = [

    re_path(r'^$', views.IndexView.as_view(), name='web.index'),
    re_path(r'^login$', views.LoginView.as_view(), name='web.login'),
    re_path(r'^logout$', views.LogoutView.as_view(), name='web.logout'),
    re_path(r'^signup$', views.SignUpView.as_view(), name='web.signup'),
    re_path(r'^ui$', views.FIndex.as_view(), name='frontend.index'),
    re_path(r'^auth$', views.auth_api),
    re_path(r'^pods$', views.PodListView.as_view(), name='web.pods'),
]
