from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from djangoldp.models import Model
from djangoldp.permissions import ReadAndCreate

from djangoldp_energiepartagee.permissions import ActorPermissions

from djangoldp_energiepartagee.models.region import *
from djangoldp_energiepartagee.models.college import *
from djangoldp_energiepartagee.models.regional_network import *
from djangoldp_energiepartagee.models.intervention_zone import *
from djangoldp_energiepartagee.models.legal_structure import *
from djangoldp_energiepartagee.models.college_epa import *
from djangoldp_energiepartagee.models.integration_step import *
from djangoldp_energiepartagee.models.discount import *

ACTORTYPE_CHOICES = [
    ("soc_citoy", "Sociétés Citoyennes"),
    ("collectivite", "Collectivités"),
    ("structure", "Structures d’Accompagnement"),
    ("partenaire", "Partenaires"),
]

CATEGORY_CHOICES = [
    ("collectivite", "Collectivités"),
    ("porteur_dev", "Porteurs de projet en développement"),
    ("porteur_exploit", "Porteurs de projet en exploitation"),
    ("partenaire", "Partenaires"),
]


class Actor(Model):
    shortname = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Nom court de l'acteur"
    )
    longname = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Nom long de l'acteur"
    )
    address = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Adresse"
    )
    complementaddress = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Complément d'adresse"
    )
    postcode = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Code Postal"
    )
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="Ville")
    region = models.ForeignKey(
        Region,
        max_length=50,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Région",
        related_name="actors",
    )
    website = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Site internet"
    )
    mail = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Adresse mail"
    )
    phone = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Numéro de téléphone"
    )
    iban = models.CharField(max_length=35, blank=True, null=True, verbose_name="IBAN")
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
    status = models.BooleanField(
        verbose_name="Adhérent", blank=True, null=True, default=False
    )
    regionalnetwork = models.ForeignKey(
        Regionalnetwork,
        blank=True,
        null=True,
        max_length=250,
        on_delete=models.SET_NULL,
        verbose_name="Paiement à effectuer à",
    )
    actortype = models.CharField(
        choices=ACTORTYPE_CHOICES,
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Type d'acteur",
    )
    category = models.CharField(
        choices=CATEGORY_CHOICES,
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Catégorie de cotisant",
    )
    numberpeople = models.IntegerField(
        blank=True, null=True, verbose_name="Nombre d'habitants"
    )
    numberemployees = models.IntegerField(
        blank=True, null=True, verbose_name="Nombre d'employés"
    )
    turnover = models.IntegerField(
        blank=True, null=True, verbose_name="Chiffre d'affaires"
    )
    presentation = models.TextField(
        blank=True, null=True, verbose_name="Présentation/objet de la structure"
    )
    interventionzone = models.ManyToManyField(
        Interventionzone,
        blank=True,
        max_length=50,
        verbose_name="Zone d'intervention",
        related_name="actors",
    )
    logo = models.CharField(
        blank=True,
        max_length=250,
        null=True,
        default="https://moncompte.energie-partagee.org/img/default_avatar_actor.svg",
        verbose_name="Logo",
    )
    legalstructure = models.ForeignKey(
        Legalstructure,
        max_length=50,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Structure Juridique",
        related_name="actors",
    )
    legalrepresentant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="%(class)s_requests_created",
        blank=True,
        null=True,
        verbose_name="Représentant légal",
    )
    managementcontact = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Contact Gestion",
    )
    adhmail = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Mail pour compte espace ADH"
    )
    siren = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="SIREN ou RNA"
    )
    collegeepa = models.ForeignKey(
        Collegeepa,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Collège EPA",
        related_name="actors",
    )
    college = models.ForeignKey(
        College,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Collège",
        related_name="actors",
    )
    actorcomment = models.TextField(
        blank=True, null=True, verbose_name="Commentaires de l'acteur"
    )
    signataire = models.BooleanField(
        blank=True, null=True, verbose_name="Signataire de la charte EP", default=False
    )
    adhesiondate = models.IntegerField(
        blank=True, null=True, verbose_name="Adhérent depuis"
    )
    renewed = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="Adhérent sur l'année en cours",
        default=True,
    )
    integrationstep = models.ForeignKey(
        Integrationstep,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Espace administrateur",
        related_name="actors",
    )
    visible = models.BooleanField(
        blank=True, null=True, verbose_name="Visible sur la carte", default=False
    )
    createdate = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )
    updatedate = models.DateTimeField(
        auto_now=True, verbose_name="Date de dernière mise à jour"
    )
    villageoise = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="réseau des Centrales Villageoises",
        default=False,
    )

    @property
    def name(self):
        if self.shortname and self.longname:
            return "%s - %s" % (self.shortname, self.longname)
        elif self.shortname:
            return "%s" % (self.shortname)
        elif self.longname:
            return "%s" % (self.longname)
        else:
            return self.urlid

    def get_next_contribution_amount(self):
        """:return: the amount an actor should contribute in their next contribution"""
        # get the amount of villageoise discount
        villageoise = Discount.objects.filter(name="villageoise").values()
        discountvillageoise = 0
        if len(villageoise):
            discountvillageoise = villageoise[0].get("amount")
        amount = 0

        # Collectivity: 2c€ * Habitants - +50€ -1000€
        if self.category == CATEGORY_CHOICES[0][0]:
            if self.numberpeople:
                amount = 0.02 * self.numberpeople
                if amount < 50 or amount == 0:
                    amount = 50
                elif amount > 1000:
                    amount = 1000
            else:
                amount = 50
        # Porteur_dev: 50€
        elif self.category == CATEGORY_CHOICES[1][0]:
            amount = 50
        # Porteur_exploit: 0.5% CA +50€ -1000€
        elif self.category == CATEGORY_CHOICES[2][0]:
            if self.turnover:
                amount = 0.005 * self.turnover
                if amount < 50:
                    amount = 50
                elif amount > 1000:
                    amount = 1000
            else:
                amount = 50
        # Partenaire:
        #   - 1 to 4 salariés: 100€
        #   - 5 to 10 salariés: 250€
        #   - > 10 salariés: 400€
        elif self.category == CATEGORY_CHOICES[3][0]:
            if self.numberemployees:
                if self.numberemployees < 5:
                    amount = 100
                elif self.numberemployees <= 10:
                    amount = 250
                elif self.numberemployees > 10:
                    amount = 400
            else:
                amount = 100
        # apply villageoise discount for the actors
        if self.villageoise is True:
            amount = amount * (100 - float(discountvillageoise)) / 100
        return amount

    class Meta(Model.Meta):
        ordering = ["shortname"]
        permission_classes = [ReadAndCreate | ActorPermissions]
        nested_fields = [
            "members",
            "integrationstep",
            "contributions",
            "capital_distributions",
            "partner_of",
        ]
        rdf_type = "energiepartagee:actor"
        verbose_name = _("Acteur")
        verbose_name_plural = _("Acteurs")

    def __str__(self):
        return self.name
