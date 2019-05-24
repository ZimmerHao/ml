from rest_framework import serializers

from apps.kauth.models import KRole


class KRoleCreateSerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=255)
    namespace = serializers.CharField(max_length=255)
    resource_id = serializers.IntegerField(write_only=True)
    verb = serializers.CharField(max_length=255, write_only=True)
    date_added = serializers.DateTimeField(format='iso-8601', read_only=True)
    date_updated = serializers.DateTimeField(format='iso-8601', read_only=True)

    class Meta:
        model = KRole
        fields = ('name', 'k8s_permission_id', 'date_added', 'date_updated')


class KRoleSerializer(serializers.ModelSerializer):
    date_added = serializers.DateTimeField(format='iso-8601', read_only=True)
    date_updated = serializers.DateTimeField(format='iso-8601', read_only=True)

    class Meta:
        model = KRole
        fields = '__all__'
