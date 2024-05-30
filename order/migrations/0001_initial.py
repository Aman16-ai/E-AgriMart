# Generated by Django 4.1.2 on 2024-05-22 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0002_cropdetail_farmerprofile'),
        ('farmer', '0008_bid_timestamp_alter_bid_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('PROCESSING', 'PROCESSING'), ('SHIPPED', 'SHIPPED'), ('DELIVERED', 'DELIVERED')], default='PENDING', max_length=20)),
                ('price', models.FloatField(blank=True, null=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_address', to='account.address')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_customer', to='account.userprofile')),
                ('farmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_farmer', to='account.userprofile')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_product', to='farmer.product')),
            ],
        ),
    ]
