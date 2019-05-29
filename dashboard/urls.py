from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'^k8s/roles', views.KRoleViewSet, base_name='dashboard.k8s_role')
urlpatterns = router.urls

urlpatterns += [
    url(r'^login$', views.LoginView.as_view(), name='dashboard.login'),
    url(r'^logout$', views.LogoutView.as_view(), name='dashboard.logout'),
    url(r'^users/(?P<pk>[0-9]+)/k8s/roles$', views.UserKRolesView.as_view(), name='dashboard.permissions'),
]
