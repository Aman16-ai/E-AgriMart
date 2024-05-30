# Generated by Django 4.1.2 on 2024-05-30 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmer', '0008_bid_timestamp_alter_bid_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(blank=True, choices=[('ordered', 'ordered'), ('unordered', 'unordered')], default='unordered', max_length=30, null=True),
        ),
    ]
