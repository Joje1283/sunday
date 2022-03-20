import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Grant, Type


class GrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grant
        fields = ['type', 'days']


class UseSerializer(serializers.Serializer):
    START_TIMES = (
        (datetime.time(hour=9), '09:00'),
        (datetime.time(hour=11), '11:00'),
        (datetime.time(hour=14), '14:00'),
    )
    END_TIMES = (
        (datetime.time(hour=13), '13:00'),
        (datetime.time(hour=16), '16:00'),
        (datetime.time(hour=18), '18:00'),
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
        data['_start_date'] = datetime.datetime(year=start_date.year,
                                                month=start_date.month,
                                                day=start_date.day,
                                                hour=start_date_time.hour)
        data['_end_date'] = datetime.datetime(year=end_date.year,
                                              month=end_date.month,
                                              day=end_date.day,
                                              hour=end_date_time.hour)
        data['days'] = self._calculate_days(start_date, start_date_time.hour, end_date, end_date_time.hour)
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
