# Generated by Django 4.0.4 on 2022-07-17 16:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_remove_auctionlisting_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
