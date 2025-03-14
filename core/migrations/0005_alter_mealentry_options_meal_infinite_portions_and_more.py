# Generated by Django 4.2.17 on 2025-03-11 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_mealentry'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mealentry',
            options={'verbose_name': 'Meal entry', 'verbose_name_plural': 'Meal entry'},
        ),
        migrations.AddField(
            model_name='meal',
            name='infinite_portions',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='meal',
            name='available_portions',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='meal',
            name='total_portions',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='mealentry',
            name='portions',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
