# Generated by Django 2.2.24 on 2022-01-28 09:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangoldp_energiepartagee', '0061_auto_20220114_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='college',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='actors', to='djangoldp_energiepartagee.College', verbose_name='Collège'),
        ),
        migrations.AlterField(
            model_name='actor',
            name='collegeepa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='actors', to='djangoldp_energiepartagee.Collegeepa', verbose_name='Collège EPA'),
        ),
        migrations.AlterField(
            model_name='actor',
            name='integrationstep',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='actors', to='djangoldp_energiepartagee.Integrationstep', verbose_name='Espace administrateur'),
        ),
        migrations.AlterField(
            model_name='actor',
            name='legalrepresentant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='actor_requests_created', to=settings.AUTH_USER_MODEL, verbose_name='Représentant légal'),
        ),
        migrations.AlterField(
            model_name='actor',
            name='legalstructure',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='actors', to='djangoldp_energiepartagee.Legalstructure', verbose_name='Structure Juridique'),
        ),
        migrations.AlterField(
            model_name='actor',
            name='managementcontact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Contact Gestion'),
        ),
        migrations.AlterField(
            model_name='actor',
            name='region',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='actors', to='djangoldp_energiepartagee.Region', verbose_name='Région'),
        ),
        migrations.AlterField(
            model_name='actor',
            name='regionalnetwork',
            field=models.ForeignKey(blank=True, max_length=250, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djangoldp_energiepartagee.Regionalnetwork', verbose_name='Paiement à effectuer à'),
        ),
        migrations.AlterField(
            model_name='contribution',
            name='actor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contributions', to='djangoldp_energiepartagee.Actor', verbose_name='Acteur'),
        ),
        migrations.AlterField(
            model_name='contribution',
            name='callcontact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='animateur régional contact'),
        ),
        migrations.AlterField(
            model_name='contribution',
            name='paymentmethod',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djangoldp_energiepartagee.Paymentmethod', verbose_name='Moyen de paiement'),
        ),
        migrations.AlterField(
            model_name='contribution',
            name='paymentto',
            field=models.ForeignKey(blank=True, max_length=250, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djangoldp_energiepartagee.Regionalnetwork', verbose_name='Paiement à effectuer à'),
        ),
        migrations.AlterField(
            model_name='contribution',
            name='receivedby',
            field=models.ForeignKey(blank=True, max_length=250, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contribution_requests_created', to='djangoldp_energiepartagee.Regionalnetwork', verbose_name='Paiement reçu par'),
        ),
        migrations.AlterField(
            model_name='contribution',
            name='ventilationto',
            field=models.ForeignKey(blank=True, max_length=250, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contribution_ventilation', to='djangoldp_energiepartagee.Regionalnetwork', verbose_name='Bénéficiaire de la ventilation'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='regionalnetwork',
            name='usercontact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='contact'),
        ),
        migrations.AlterField(
            model_name='relatedactor',
            name='actor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members', to='djangoldp_energiepartagee.Actor', verbose_name='Acteur'),
        ),
        migrations.AlterField(
            model_name='relatedactor',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
