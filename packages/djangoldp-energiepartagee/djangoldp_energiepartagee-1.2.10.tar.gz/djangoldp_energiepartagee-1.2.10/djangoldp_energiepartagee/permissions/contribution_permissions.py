from djangoldp.permissions import LDPBasePermission
from djangoldp_energiepartagee.filters import ContributionFilterBackend


class ContributionPermissions(LDPBasePermission):
    filter_backend = ContributionFilterBackend
    permissions = {"view"}

    def get_filter_backend(cls, model):
        return cls.filter_backend

    def has_object_permission(self, request, view, obj=None):
        # Start with checking if access to the object is allowed based on LDPBasePermission logic
        if not super().has_object_permission(request, view, obj):
            return False

        # Additional custom logic for ContributionPermissions
        if request.user.is_superuser:
            return True

        # Ensure user is authenticated
        from djangoldp_energiepartagee.models.related_actor import Relatedactor

        if request.user and request.user.is_authenticated:
            admin_actor_pks = Relatedactor.get_mine(
                user=request.user, role="admin"
            ).values_list("pk", flat=True)
            member_actor_pks = Relatedactor.get_mine(
                user=request.user, role="membre"
            ).values_list("pk", flat=True)

            if obj.actor.pk in admin_actor_pks:
                return request.method in [
                    "GET",
                    "PUT",
                    "PATCH",
                ]  # Admins can view, change
            elif obj.actor.pk in member_actor_pks:
                return request.method == "GET"  # Members can view

        return False
