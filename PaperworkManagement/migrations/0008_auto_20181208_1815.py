# Generated by Django 2.1.2 on 2018-12-08 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PaperworkManagement', '0007_auto_20181208_1759'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dbppw',
            name='reportstatus',
        ),
        migrations.RemoveField(
            model_name='dbppw',
            name='stats_views',
        ),
    ]
