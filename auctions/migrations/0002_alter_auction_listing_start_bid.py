# Generated by Django 4.0.3 on 2023-02-09 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listing',
            name='start_bid',
            field=models.IntegerField(max_length=65),
        ),
    ]