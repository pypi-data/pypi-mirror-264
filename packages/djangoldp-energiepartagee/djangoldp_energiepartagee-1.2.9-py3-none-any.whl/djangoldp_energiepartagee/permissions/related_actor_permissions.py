from djangoldp.permissions import LDPBasePermission
from djangoldp_energiepartagee.filters import RelatedactorFilterBackend


####
# Only the admin of an actor can modify it (and superusers of course)
# Members can view the actor
####
class RelatedactorPermissions(LDPBasePermission):
    permissions = {"view", "add", "change", "delete"}

    filter_backend = RelatedactorFilterBackend

    def get_filter_backend(cls, model):
        return cls.filter_backend

    def has_permission(self, request, view):
        if request.method == "OPTIONS":
            return True
        if request.user.is_anonymous:
            return False
        from djangoldp_energiepartagee.models.related_actor import Relatedactor

        # Allow container-level 'add' action for authenticated users.
        if request.method == "POST":
            role = request.data.get("role")
            if role in ("admin", "membre", "refused"):
                actor_urlid = request.data.get("actor")["@id"]
                if actor_urlid:
                    return Relatedactor.objects.filter(
                        actor__urlid=actor_urlid,
                        user=request.user,
                        role__in=("admin", "membre"),
                    ).exists()
                return False  # If no actor ID is provided, deny permission
            elif role is None and request.user.is_authenticated:
                return True

        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj=None):
        if request.method == "OPTIONS":
            return True
        if request.user.is_anonymous:
            return False
        from djangoldp_energiepartagee.models.related_actor import Relatedactor

        # Call super to keep default LDPBasePermission checks
        if not super().has_object_permission(request, view, obj):
            return False

        # Direct permission if the user is the same as the object's user
        if request.user == obj.user:
            if obj.role == "admin":
                return request.method in ["GET", "PUT", "PATCH", "DELETE", "POST"]
            elif obj.role == "membre" or obj.role is None or obj.role == "":
                return request.method == "GET"

        # Additional checks for admin/member roles related to the actor
        if hasattr(obj, "actor") and obj.actor is not None:
            user_actors_ids = Relatedactor.get_user_actors_id(
                user=request.user, role="admin"
            )
            if obj.actor.id in user_actors_ids:
                return request.method in ["GET", "PUT", "PATCH", "DELETE", "POST"]

        #     user_actors_ids = Relatedactor.get_user_actors_id(user=request.user)
        #     if obj.actor.id in user_actors_ids:
        #         return request.method == 'GET'

        # Default to False if none of the above conditions are met
        return False
