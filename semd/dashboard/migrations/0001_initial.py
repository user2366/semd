# Generated by Django 5.1.3 on 2024-11-16 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='semd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='СЭМД')),
            ],
            options={
                'verbose_name': 'СЭМД',
                'verbose_name_plural': 'СЭМДы',
            },
        ),
    ]