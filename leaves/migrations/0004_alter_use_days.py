# Generated by Django 4.0.3 on 2022-03-20 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0003_alter_use_approve_alter_use_cancel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='use',
            name='days',
            field=models.FloatField(verbose_name='사용한 휴가 일수'),
        ),
    ]