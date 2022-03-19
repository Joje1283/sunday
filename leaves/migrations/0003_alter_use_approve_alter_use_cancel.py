# Generated by Django 4.0.3 on 2022-03-19 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0002_alter_use_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='use',
            name='approve',
            field=models.BooleanField(default=False, verbose_name='휴가 승인 여부'),
        ),
        migrations.AlterField(
            model_name='use',
            name='cancel',
            field=models.BooleanField(default=False, verbose_name='휴가 취소 여부'),
        ),
    ]
