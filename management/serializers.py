from rest_framework import serializers
from leaves.models import Use


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Use
        fields = ['id', 'user', 'type', 'days', 'start_date', 'end_date', 'approve']
        read_only_fields = ['user', 'type', 'days', 'start_date', 'end_date']
