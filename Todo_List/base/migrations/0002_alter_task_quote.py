# Generated by Django 4.2.4 on 2023-09-03 05:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="quote",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
