# Generated by Django 4.2.6 on 2023-10-19 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="advance_paid",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
