# Generated by Django 3.0.5 on 2020-04-26 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0007_auto_20200426_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='syncstatus',
            name='sync_end_time',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
