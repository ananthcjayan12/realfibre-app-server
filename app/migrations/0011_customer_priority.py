# Generated by Django 4.2.6 on 2023-10-23 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0010_rename_advance_balance_amount_customer_balance_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="priority",
            field=models.CharField(
                choices=[("HIGH", "HIGH"), ("LESS", "LESS")],
                default="high",
                max_length=20,
            ),
        ),
    ]
