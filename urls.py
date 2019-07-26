"""arena URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.views import auth_logout

urlpatterns = [
    path(r"api/v1/users/", include("apps.user.urls")),
    path(r"api/v1/kops/", include("apps.kops.urls")),
    path(r"dashboard/", include("dashboard.urls")),
    path(r"hi/", include("web.urls")),
    path(r"chat/", include("apps.chat.urls")),
    path(r"hi/", include("apps.kops.urls")),
    path(r"hi/", include("apps.console.urls")),
    path(r"app/", include("apps.console.urls")),
    path(r"admin/", admin.site.urls),
    path(r"oauth/", include('social_django.urls', namespace='social')),
    path(r"logout/", auth_logout, {'next_page': settings.LOGOUT_REDIRECT_URL},
         name='logout')
]

