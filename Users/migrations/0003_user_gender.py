# Generated by Django 3.2.6 on 2022-01-07 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_auto_20220107_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(max_length=16, null=True),
        ),
    ]
