from .models import Pod
from .serializers import PodSerializer
from rest_framework import generics

class PodListCreate(generics.ListCreateAPIView):
    queryset = Pod.objects.all()
    serializer_class = PodSerializer