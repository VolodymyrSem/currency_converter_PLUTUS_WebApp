# Generated by Django 4.2.1 on 2023-05-19 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PreparedCurrencies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_currency', models.CharField(max_length=255)),
                ('to_currency', models.CharField(max_length=255)),
                ('rate', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SavedPairs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_currency', models.CharField(max_length=255)),
                ('to_currency', models.CharField(max_length=255)),
                ('amount', models.FloatField()),
            ],
        ),
    ]
