# Generated by Django 4.1.2 on 2023-11-27 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmer', '0006_alter_product_quality'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='title',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
