import datetime
import pytz

from django.utils import timezone
from django.db.models import Sum
from django.conf import settings

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Grant, Type, Use


def get_residual_leave_count(user_id, type):
    granted_leave_count = Grant.objects.filter(
        user_id=user_id,
        type=type,
    ).count()
    used_leave_qs = Use.objects.filter(
        user_id=user_id,
        type=type,
        approve=True,
        cancel=False
    )
    used_leave_count = used_leave_qs.aggregate(Sum('days')).get('days__sum', 0) if used_leave_qs else 0
    return granted_leave_count - used_leave_count


class LeaveCountSerializer(serializers.Serializer):
    count = serializers.FloatField()


class GrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grant
        fields = ['type', 'days']


class UseSerializer(serializers.Serializer):
    START_TIMES = (
        (datetime.time(hour=9, tzinfo=pytz.timezone(settings.TIME_ZONE)), '09:00'),
        (datetime.time(hour=11, tzinfo=pytz.timezone(settings.TIME_ZONE)), '11:00'),
        (datetime.time(hour=14, tzinfo=pytz.timezone(settings.TIME_ZONE)), '14:00'),
    )
    END_TIMES = (
        (datetime.time(hour=13, tzinfo=pytz.timezone(settings.TIME_ZONE)), '13:00'),
        (datetime.time(hour=16, tzinfo=pytz.timezone(settings.TIME_ZONE)), '16:00'),
        (datetime.time(hour=18, tzinfo=pytz.timezone(settings.TIME_ZONE)), '18:00'),
    )
    type = serializers.ChoiceField(choices=Type.choices, default=Type.ANNURE)
    start_date = serializers.DateField()
    start_date_time = serializers.ChoiceField(choices=START_TIMES, default=START_TIMES[0][0])
    end_date = serializers.DateField()
    end_date_time = serializers.ChoiceField(choices=END_TIMES, default=END_TIMES[-1][0])

    def validate(self, data):
        start_date, end_date = data['start_date'], data['end_date']
        start_date_time, end_date_time = data['start_date_time'], data['end_date_time']
        if start_date > end_date:
            raise ValidationError('휴가 종료일이 휴가 시작일보다 빠릅니다.')
        data['_start_date'] = timezone.datetime(year=start_date.year,
                                                month=start_date.month,
                                                day=start_date.day,
                                                hour=start_date_time.hour,
                                                tzinfo=pytz.timezone(settings.TIME_ZONE))
        data['_end_date'] = timezone.datetime(year=end_date.year,
                                              month=end_date.month,
                                              day=end_date.day,
                                              hour=end_date_time.hour,
                                              tzinfo=pytz.timezone(settings.TIME_ZONE))
        data['days'] = self._calculate_days(start_date, start_date_time.hour, end_date, end_date_time.hour)
        user_id = self.context['request'].user.pk
        residual_leave_count = get_residual_leave_count(user_id, data['type'])
        if data['days'] > residual_leave_count:
            raise ValidationError(f'잔여 휴가(type: {data["type"]})가 부족합니다.')
        return data

    @staticmethod
    def _calculate_days(start_date, start_date_time_hour, end_date, end_date_time_hour):
        result = (end_date - start_date).days
        if start_date_time_hour == 11:
            result -= 0.25
        elif start_date_time_hour == 14:
            result -= 0.5

        if end_date_time_hour == 13:
            result -= 0.5
        elif end_date_time_hour == 16:
            result -= 0.25
        return result

    @property
    def result(self):
        data = self.validated_data
        return {
            'type': data['type'],
            'days': data['days'],
            'start_date': data['_start_date'],
            'end_date': data['_end_date'],
        }
