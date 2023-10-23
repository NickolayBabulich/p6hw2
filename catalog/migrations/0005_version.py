# Generated by Django 4.2.5 on 2023-10-23 06:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_alter_product_date_create_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version_number', models.PositiveIntegerField(verbose_name='номер версии')),
                ('version_name', models.CharField(max_length=150, verbose_name='название версии')),
                ('actual_version', models.BooleanField(default=False, verbose_name='текущая версия')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='продукт')),
            ],
            options={
                'verbose_name': 'версия',
                'verbose_name_plural': 'версии',
            },
        ),
    ]