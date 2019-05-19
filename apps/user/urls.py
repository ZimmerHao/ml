from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
urlpatterns = router.urls

urlpatterns += [
    url(r'^login$', views.LoginView.as_view(), name='api.user.login'),
    url(r'^logout$', views.LogoutView.as_view(), name='api.user.logout'),
    url(r'^signup$', views.SignUpView.as_view(), name='api.user.signup'),
    url(r'^vcode$', views.VCodeView.as_view(), name='api.user.vcode'),
    url(r'^vcode/check$', views.VCodeCheckView.as_view(), name='api.user.vcode.check'),
    url(r'^password$', views.PasswordResetView.as_view(), name='api.user.password.reset'),
    url(r'^phone', views.UserPhoneView.as_view(), name='api.user.phone'),
]
