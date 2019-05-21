from rest_framework import serializers

from apps.kauth.models import KPermission, KRole


class KPermissionCreateSerializer(serializers.ModelSerializer):
    resource = serializers.CharField(max_length=255)
    verb = serializers.CharField(max_length=255)
    date_added = serializers.DateTimeField(format='iso-8601', read_only=True)
    date_updated = serializers.DateTimeField(format='iso-8601', read_only=True)

    class Meta:
        model = KPermission
        fields = ('resource', 'verb', 'date_added', 'date_updated')


class KPermissionSerializer(serializers.ModelSerializer):
    date_added = serializers.DateTimeField(format='iso-8601', read_only=True)
    date_updated = serializers.DateTimeField(format='iso-8601', read_only=True)

    class Meta:
        model = KPermission
        fields = '__all__'


class KRoleCreateSerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=255)
    k8s_permission_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )
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
