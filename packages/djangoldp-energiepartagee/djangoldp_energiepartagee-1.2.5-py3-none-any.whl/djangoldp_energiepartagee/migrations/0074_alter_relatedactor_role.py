# Generated by Django 4.2.7 on 2024-02-11 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoldp_energiepartagee', '0073_relatedactor_reminderdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relatedactor',
            name='role',
            field=models.CharField(blank=True, choices=[('admin', 'Administrateur'), ('membre', 'Membre'), ('refuse', 'Refusé')], default='', max_length=50, verbose_name="Rôle de l'utilisateur"),
        ),
    ]
