# Generated by Django 4.2.17 on 2025-02-03 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('kcal', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='kcal/100g')),
                ('protein', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='protein/100g')),
                ('fat', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='fat/100g')),
                ('carbs', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='carbs/100g')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grams', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='grams')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.product')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.recipe')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='products',
            field=models.ManyToManyField(related_name='recipes', through='core.RecipeProduct', to='core.product'),
        ),
    ]
