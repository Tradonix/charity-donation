# Generated by Django 3.0.8 on 2020-07-14 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='type',
            field=models.CharField(choices=[('FU', 'fundacja'), ('OP', 'organizacja porządkowa'), ('ZL', 'zbiórka lokalna')], default=1, max_length=2),
        ),
    ]
