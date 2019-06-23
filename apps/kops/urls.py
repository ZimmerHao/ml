from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
urlpatterns = router.urls

urlpatterns += [
    path('pod_log/', views.PodLogView.as_view(), name='api.kops.pod_log'),
    path('apply_yaml/', views.ApplyYamlView.as_view(), name='api.kops.apply_yaml'),
]
