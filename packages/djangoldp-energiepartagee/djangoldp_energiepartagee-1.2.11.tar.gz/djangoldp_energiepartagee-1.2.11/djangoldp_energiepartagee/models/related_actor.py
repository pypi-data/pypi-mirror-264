from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from djangoldp.models import Model
from djangoldp.utils import is_anonymous_user
from djangoldp.views import LDPViewSet

from djangoldp_energiepartagee.permissions import RelatedactorPermissions

from djangoldp_energiepartagee.models.actor import *


ROLE_CHOICES = [("admin", "Administrateur"), ("membre", "Membre"), ("refuse", "Refusé")]


class RelatedactorViewSet(LDPViewSet):
    def is_safe_create(self, user, validated_data, *args, **kwargs):
        """
        A function which is checked before the create operation to confirm the validated data is safe to add
        returns False by default
        returns True if the user:
            - is superuser
            - is admin or member on any actor
            - is unknown (that is a user without any relatedactor) user and tries to add a relatedactor with an empty role
        """

        # is superuser
        if user.is_superuser:
            return True

        try:
            # from djangoldp_energiepartagee.models import Relatedactor
            # is admin or member on any actor
            if Relatedactor.objects.filter(
                user=user, role__in=["admin", "member"]
            ).exists():
                return True

            # is unknown user and tries to add a relatedactor with an empty role
            if (
                not Relatedactor.objects.filter(user=user).exists()
                and validated_data.get("role") == None
            ):
                return True

        except (get_user_model().DoesNotExist, KeyError):
            pass

        return False


class Relatedactor(Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE
    )
    actor = models.ForeignKey(
        Actor,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Acteur",
        related_name="members",
    )
    role = models.CharField(
        choices=ROLE_CHOICES,
        max_length=50,
        blank=True,
        default="",
        verbose_name="Rôle de l'utilisateur",
    )
    createdate = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )
    reminderdate = models.DateTimeField(
        blank=True, null=True, verbose_name="Date de relance"
    )

    class Meta(Model.Meta):
        ordering = ["pk"]
        permission_classes = [RelatedactorPermissions]
        view_set = RelatedactorViewSet
        rdf_type = "energiepartagee:relatedactor"
        unique_together = ["user", "actor"]
        verbose_name = _("Membre")
        verbose_name_plural = _("Membres")
        depth = 2

    def __str__(self):
        if self.actor and self.user and self.user.first_name:
            return "%s - %s" % (self.user.first_name, self.actor)
        else:
            return self.urlid

    @classmethod
    def get_mine(self, user, role=None):
        if is_anonymous_user(user):
            return Relatedactor.objects.none()

        if role is None:
            return Relatedactor.objects.filter(user=user)

        return Relatedactor.objects.filter(user=user, role=role)

    @classmethod
    def get_user_actors_id(self, user, role=None):
        return self.get_mine(user=user, role=role).values_list("actor_id", flat=True)
