# Generated by Django 4.0.4 on 2022-06-19 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nifleur', '0002_alter_schoolyear_label_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolyear',
            name='structure_campus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='structure_school_year', to='nifleur.structurecampus', verbose_name='Ecole'),
        ),
    ]