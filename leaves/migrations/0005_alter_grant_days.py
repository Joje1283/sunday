# Generated by Django 4.0.3 on 2022-03-20 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0004_alter_use_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grant',
            name='days',
            field=models.FloatField(verbose_name='부여된 휴가 일수'),
        ),
    ]
