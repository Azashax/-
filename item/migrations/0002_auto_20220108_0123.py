# Generated by Django 3.2.6 on 2022-01-07 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemmodel',
            name='mydes_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='itemmodel',
            name='mydes_uz',
            field=models.TextField(null=True),
        ),
    ]
