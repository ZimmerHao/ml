from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('zeppelin', RedirectView.as_view(url='http://console.deepvega.com/hi/zeppelin/tony'), name='api.console.zeppelin' ),
    path('zeppelin2', views.ZeppelinView.as_view(), name='api.console.zeppelin2' ),
    path('zeppelin3', RedirectView.as_view(url='http://console.deepvega.com/app/zeppelin/tony'), name='api.console.zeppelin3' ),
    path('zeppelin4', views.ZeppelinView4.as_view(), name='api.console.zeppelin4' ),
    # path('zeppelin/tony', views.ZeppelinView5.as_view(), name='api.console.zeppelin5' ),

]