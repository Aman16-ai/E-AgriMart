# Generated by Django 4.1.2 on 2023-06-30 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmer', '0003_remove_bid_farmer_bid_crop'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quality',
            field=models.CharField(blank=True, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], max_length=30, null=True),
        ),
    ]
