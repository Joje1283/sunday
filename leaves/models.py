from django.db import models
from django.conf import settings


class Type(models.TextChoices):
    ANNURE = 'A'
    UNPAID = 'U'
    FAMILY_EVENT = 'F'
    SPECIAL = 'S'


class Grant(models.Model):
    user = models.ForeignKey(
        verbose_name='대상 유저',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING
    )
    type = models.CharField(
        verbose_name='연차 종류',
        max_length=1,
        choices=Type.choices,
        default=Type.ANNURE,
    )
    days = models.FloatField(
        verbose_name='부여된 휴가 일수'
    )


class Use(models.Model):
    user = models.ForeignKey(
        verbose_name='대상 유저',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING
    )
    type = models.CharField(
        verbose_name='연차 종류',
        max_length=1,
        choices=Type.choices,
        default=Type.ANNURE
    )
    days = models.FloatField(
        verbose_name='사용한 휴가 일수'
    )
    start_date = models.DateTimeField(verbose_name='휴가 시작일')
    end_date = models.DateTimeField(verbose_name='휴가 종료일')
    approve = models.BooleanField(verbose_name='휴가 승인 여부', default=False)
    cancel = models.BooleanField(verbose_name='휴가 취소 여부', default=False)
