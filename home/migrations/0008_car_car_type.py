# Generated by Django 4.0.6 on 2024-04-09 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_car_added_by_shippingaddress_days_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='car_type',
            field=models.CharField(choices=[('U', 'Used'), ('N', 'New')], default='U', max_length=1),
        ),
    ]
