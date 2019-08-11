from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/pod_log/(?P<pod_name>[^/]+)/$', consumers.LogConsumer),
]
