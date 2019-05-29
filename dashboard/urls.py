from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'k8s/roles', views.KRoleViewSet, base_name='dashboard.k8s_role')
urlpatterns = router.urls

urlpatterns += [
    path('login/', views.LoginView.as_view(), name='dashboard.login'),
    path('logout/', views.LogoutView.as_view(), name='dashboard.logout'),
    path('users/<int:pk>/k8s/roles/', views.UserKRolesView.as_view(), name='dashboard.permissions'),
]
