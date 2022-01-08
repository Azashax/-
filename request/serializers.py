import re

from rest_framework import serializers

from request.models import RequestModel


class RequestSerializer(serializers.ModelSerializer):
    def validate_phone(self, value):
        matched = re.match(r'^\+998\d{9}$', value)

        if not matched:
            raise serializers.ValidationError({'message': 'Incorrect phone number format', 'status': False})
        return value

    class Meta:
        model = RequestModel
        fields = ['full_name', 'organization', 'phone', 'comment']
