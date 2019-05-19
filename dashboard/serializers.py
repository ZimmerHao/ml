from rest_framework import serializers


from apps.user.models import User


class UserBaseSerializer(serializers.ModelSerializer):

    date_added = serializers.DateTimeField(format='iso-8601', read_only=True)
    date_updated = serializers.DateTimeField(format='iso-8601', read_only=True)

    class Meta:
        model = User
        fields = '__all__'
