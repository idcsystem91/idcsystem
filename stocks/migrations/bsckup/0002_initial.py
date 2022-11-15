# Generated by Django 4.0.6 on 2022-07-26 05:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stocks', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='stockdata',
            name='staff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='担当者'),
        ),
        migrations.AddField(
            model_name='stockdata',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='stocks.status', verbose_name='状態'),
        ),
        migrations.AddField(
            model_name='device',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.service', verbose_name='サービス'),
        ),
        migrations.AddField(
            model_name='device',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.type', verbose_name='種別'),
        ),
    ]
