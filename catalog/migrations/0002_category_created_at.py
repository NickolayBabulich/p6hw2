# Generated by Django 4.2.5 on 2023-09-26 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='дата создания'),
        ),
    ]
