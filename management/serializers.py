from rest_framework import serializers
from leaves.models import Use


class LeaveListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Use
        fields = ['user', 'type', 'days', 'start_date', 'end_date', 'approve']
