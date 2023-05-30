# Generated by Django 4.0.3 on 2023-02-12 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_bids'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction_listing',
            name='creator',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='auction_listing',
            name='start_bid',
            field=models.IntegerField(),
        ),
    ]