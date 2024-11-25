# Generated by Django 4.2.6 on 2023-10-19 17:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("location", models.CharField(max_length=255)),
                (
                    "advance_paid",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                ("form_complete", models.BooleanField(default=False)),
                (
                    "agent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Door",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.customer"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DoorOpen",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "direction",
                    models.CharField(
                        choices=[("out", "Out"), ("in", "In")], max_length=3
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Finish",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("front", models.CharField(max_length=20)),
                ("back", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Frame",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("Small", "Small"),
                            ("Normal", "Normal"),
                            ("Medium", "Medium"),
                            ("Heavy", "Heavy"),
                            ("DoorWithoutClearence", "DoorWithoutClearence"),
                            ("DoorWithClearence", "DoorWithClearence"),
                        ],
                        max_length=20,
                    ),
                ),
                ("top_measurement", models.FloatField()),
                ("breadth_measurement", models.FloatField()),
                ("height_measurement", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="Hinge",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("RH", "RH"), ("LH", "LH")], max_length=2
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Lock",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("Round", "Round"),
                            ("Latch", "Latch"),
                            ("Motislock", "Motislock"),
                            ("ALLdroplock", "ALLdroplock"),
                        ],
                        max_length=20,
                    ),
                ),
                ("sub_type", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Measurement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("top", models.FloatField()),
                ("bottom", models.FloatField()),
                ("height", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="GlassType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("glass_name", models.CharField(max_length=100)),
                (
                    "door",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.door"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DoorModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("model_name", models.CharField(max_length=100)),
                (
                    "door",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.door"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="door",
            name="door_open_selection",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="app.dooropen",
            ),
        ),
        migrations.AddField(
            model_name="door",
            name="finish_selection",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="app.finish",
            ),
        ),
        migrations.AddField(
            model_name="door",
            name="frame_selection",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="app.frame",
            ),
        ),
        migrations.AddField(
            model_name="door",
            name="hinge_selection",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="app.hinge",
            ),
        ),
        migrations.AddField(
            model_name="door",
            name="lock_selection",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="app.lock",
            ),
        ),
        migrations.AddField(
            model_name="door",
            name="measurement",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="app.measurement",
            ),
        ),
        migrations.CreateModel(
            name="ColorCombination",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("color_name", models.CharField(max_length=100)),
                (
                    "door",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.door"
                    ),
                ),
            ],
        ),
    ]
