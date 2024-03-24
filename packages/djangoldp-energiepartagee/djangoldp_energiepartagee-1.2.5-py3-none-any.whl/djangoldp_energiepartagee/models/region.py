from django.db import models
from django.utils.translation import gettext_lazy as _

from djangoldp.models import Model
from djangoldp.permissions import ReadOnly, AnonymousReadOnly


class Region(Model):
    name = models.CharField(max_length=30, blank=True, null=True, verbose_name="Région")
    isocode = models.CharField(
        max_length=6, blank=True, null=True, verbose_name="code ISO"
    )
    acronym = models.CharField(
        max_length=6, blank=True, null=True, verbose_name="Acronyme"
    )

    class Meta(Model.Meta):
        ordering = ["pk"]
        permission_classes = [
            AnonymousReadOnly & ReadOnly
        ]  # |AuthenticatedOnly,ReadOnly
        rdf_type = "energiepartagee:region"
        serializer_fields = ["name", "isocode", "acronym"]
        verbose_name = _("Région")
        verbose_name_plural = _("Régions")

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.urlid
