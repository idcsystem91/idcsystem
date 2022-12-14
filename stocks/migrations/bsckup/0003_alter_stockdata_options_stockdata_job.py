# Generated by Django 4.0.6 on 2022-07-26 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('stocks', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stockdata',
            options={'verbose_name': '在庫リスト', 'verbose_name_plural': '在庫リスト'},
        ),
        migrations.AddField(
            model_name='stockdata',
            name='job',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.job', verbose_name='業種'),
        ),
    ]
