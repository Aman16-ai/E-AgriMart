# Generated by Django 4.1.2 on 2023-06-30 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmer', '0005_bid_farmer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quality',
            field=models.CharField(blank=True, choices=[('Good', 'Good'), ('Medium', 'Medium'), ('Low', 'Low')], max_length=30, null=True),
        ),
    ]
