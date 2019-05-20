from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'k8s/perms', views.PermissionViewSet, base_name='dashboard.permission')
urlpatterns = router.urls

urlpatterns += [
    url(r'^login$', views.LoginView.as_view(), name='dashboard.login'),
    url(r'^logout$', views.LogoutView.as_view(), name='dashboard.logout'),
    url(r'^users/(?P<id>[0-9]+)/k8s/perms',
        views.UserK8sPermissionsView.as_view(),
        name='dashboard.permissions'),
    url(r'^users/k8s/perms/(?P<id>[0-9]+)',
        views.UserK8sPermissionDetailView.as_view(),
        name='dashboard.permission_detail'),
]
