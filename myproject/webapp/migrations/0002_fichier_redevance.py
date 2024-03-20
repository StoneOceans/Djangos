# Generated by Django 4.2.4 on 2024-02-28 20:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("webapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Fichier",
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
                ("nom", models.CharField(max_length=100)),
                ("contenu", models.FileField(upload_to="fichiers/")),
                ("temps", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name="Redevance",
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
                ("creation_date", models.DateTimeField(auto_now_add=True)),
                ("flpl_call_sign", models.CharField(max_length=9)),
                ("flpl_depr_airp", models.CharField(max_length=4)),
                ("flpl_arrv_airp", models.CharField(max_length=4)),
                ("airc_type", models.CharField(max_length=25)),
                ("aobt", models.IntegerField()),
            ],
        ),
    ]
