# Generated by Django 4.1.4 on 2023-12-19 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_listing_latest_price_remove_listing_link_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='condition',
            field=models.CharField(default=0, max_length=250),
        ),
    ]
