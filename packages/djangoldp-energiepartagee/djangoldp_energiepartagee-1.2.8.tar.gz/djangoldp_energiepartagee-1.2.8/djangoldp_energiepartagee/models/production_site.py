from django.db import models
from django.utils.translation import gettext_lazy as _

from djangoldp.models import Model
from djangoldp.permissions import AuthenticatedOnly, ReadOnly

from djangoldp_energiepartagee.models.citizen_project import CitizenProject
from djangoldp_energiepartagee.models.region import Region


class ProductionSite(Model):
    citizen_project = models.ForeignKey(
        CitizenProject,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Projet citoyen",
        related_name="production_sites",
    )
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    reference_unit = models.TextField(
        blank=True, null=True, verbose_name="Unité de référence"
    )
    progress_status = models.TextField(
        blank=True, null=True, verbose_name="Description"
    )
    total_development_budget = models.TextField(
        blank=True, null=True, verbose_name="Description"
    )
    total_investment_budget = models.TextField(
        blank=True, null=True, verbose_name="Description"
    )
    yearly_turnover = models.TextField(
        blank=True, null=True, verbose_name="Description"
    )
    address = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Adresse"
    )
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="Ville")
    department = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Département"
    )
    region = models.ForeignKey(
        Region,
        max_length=50,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Région",
        related_name="production_sites",
    )
    lat = models.DecimalField(
        max_digits=30,
        decimal_places=25,
        blank=True,
        null=True,
        verbose_name="Lattitude",
    )
    lng = models.DecimalField(
        max_digits=30,
        decimal_places=25,
        blank=True,
        null=True,
        verbose_name="Longitude",
    )
    expected_commissionning_yearl = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Année de mise en service prévue",
    )
    effective_commissionning_yearl = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Année de mise en service effective",
    )
    picture = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Photo"
    )
    investment_capacity_ratio = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Ratio investissement par puissance €/kW",
    )
    grants_earned_amount = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Montant des subventions reçues pour le Site de production (en €)",
    )
    production_tracking_url = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="URL monitoring du site de production",
    )

    class Meta(Model.Meta):
        ordering = ["pk"]
        permission_classes = [AuthenticatedOnly, ReadOnly]
        rdf_type = "energiepartagee:production_site"
        nested_fields = ["partner_links"]
        verbose_name = _("Site de production")
        verbose_name_plural = _("Sites de productions")

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.urlid
