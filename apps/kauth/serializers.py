from rest_framework import serializers

from apps.kauth.models import KRole


class KRoleCreateSerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=255)
    namespace = serializers.CharField(max_length=255)
    resource_id = serializers.IntegerField(write_only=True)
    verbs = serializers.ListField(child=serializers.CharField(max_length=255))
    date_added = serializers.DateTimeField(format='iso-8601', read_only=True)
    date_updated = serializers.DateTimeField(format='iso-8601', read_only=True)

    class Meta:
        model = KRole
        fields = ('name', 'namespace', 'resource_id', 'verbs', 'date_added', 'date_updated')


class KRoleUpdateSerializer(serializers.ModelSerializer):

    name = serializers.ReadOnlyField()
    namespace = serializers.ReadOnlyField()
    verbs = serializers.ListField(child=serializers.CharField(max_length=255))
    date_added = serializers.DateTimeField(format='iso-8601', read_only=True)
    date_updated = serializers.DateTimeField(format='iso-8601', read_only=True)

    class Meta:
        model = KRole
        fields = ('name', 'namespace', 'k8s_resources', 'verbs', 'date_added', 'date_updated')


class KRoleSerializer(serializers.ModelSerializer):
    date_added = serializers.DateTimeField(format='iso-8601', read_only=True)
    date_updated = serializers.DateTimeField(format='iso-8601', read_only=True)

    class Meta:
        model = KRole
        fields = '__all__'
