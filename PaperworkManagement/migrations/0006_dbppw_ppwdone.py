# Generated by Django 2.1.2 on 2018-11-29 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PaperworkManagement', '0005_auto_20181128_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='dbppw',
            name='ppwdone',
            field=models.BooleanField(default=False),
        ),
    ]