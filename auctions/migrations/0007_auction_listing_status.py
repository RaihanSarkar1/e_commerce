# Generated by Django 4.0.3 on 2023-02-12 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_auction_listing_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction_listing',
            name='status',
            field=models.CharField(default='active', max_length=6),
        ),
    ]
