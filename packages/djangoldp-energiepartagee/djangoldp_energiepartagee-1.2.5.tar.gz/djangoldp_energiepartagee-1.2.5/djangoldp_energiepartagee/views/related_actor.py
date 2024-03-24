from django.contrib.auth import get_user_model
from djangoldp.views import LDPViewSet

from djangoldp_energiepartagee.permissions import *
from djangoldp_energiepartagee.filters import *

from djangoldp_energiepartagee.models.related_actor import Relatedactor


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
