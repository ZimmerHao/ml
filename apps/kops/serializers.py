from rest_framework import serializers
from .models import Pod
class PodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pod
        fields = '__all__'