from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
urlpatterns = router.urls

urlpatterns += [
    path('login/', views.LoginView.as_view(), name='api.user.login'),
    path('logout/', views.LogoutView.as_view(), name='api.user.logout'),
    path('callback/', views.CallbackView.as_view(), name='api.user.callback'),
    path('signup/', views.SignUpView.as_view(), name='api.user.signup'),
    path('password/', views.PasswordResetView.as_view(), name='api.user.password.reset'),
]



