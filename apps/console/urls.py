from django.urls import path
from . import views
urlpatterns = [
    path('pods/', views.PodListCreate.as_view(), name='api.console.pods' ),
]