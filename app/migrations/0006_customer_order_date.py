# Generated by Django 4.2.6 on 2023-10-20 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0005_alter_frame_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="order_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
