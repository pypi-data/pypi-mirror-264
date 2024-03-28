from djangoldp.permissions import LDPBasePermission


####
# Only the admin of an actor can modify it (and superusers of course)
# Members can view the actor
####
class ActorPermissions(LDPBasePermission):
    permissions = {"add"}

    def get_permissions(self, user, model, obj=None):
        if user.is_anonymous:
            return {}

        """returns the permissions the user has on a given model or on a given object"""
        perms = super().get_permissions(user, model, obj)
        if user.is_superuser:
            return perms.union({"view", "add", "change", "delete"})

        if obj and self.is_admin(user, obj):
            return perms.union({"view", "add", "change", "delete"})

        if obj and self.is_member_or_admin(user, obj):
            return perms.union({"view", "add"})

        return perms

    def has_permission(self, request, view):
        if request.method == "OPTIONS":
            return True
        if request.user.is_anonymous:
            return False
        # First, allow all GET requests by members or admins.
        if request.method == "GET":
            return self.is_member_or_admin(request.user)
        # For PUT/PATCH requests, ensure the user is an admin.
        elif request.method in ["PUT", "PATCH"]:
            return self.is_admin(request.user)
        # You can add logic for other methods if needed.
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method == "OPTIONS":
            return True
        if request.user.is_anonymous:
            return False
        # For GET requests, check if the user is a member or an admin for the given object.
        if request.method == "GET":
            return self.is_member_or_admin(request.user, obj)
        # For PUT/PATCH requests, ensure the user is an admin for the given object.
        elif request.method in ["PUT", "PATCH"]:
            return self.is_admin(request.user, obj)
        else:
            return False

    def is_member_or_admin(self, user, obj=None):
        from djangoldp_energiepartagee.models.related_actor import Relatedactor

        """Check if the user is a member or admin. If obj is provided, check is specific to that object."""
        role_filter = {"user": user, "role__in": ["membre", "admin"]}
        if obj:
            role_filter["actor"] = obj
        return Relatedactor.objects.filter(**role_filter).exists()

    def is_admin(self, user, obj=None):
        from djangoldp_energiepartagee.models.related_actor import Relatedactor

        """Check if the user is an admin. If obj is provided, check is specific to that object."""
        role_filter = {"user": user, "role": "admin"}
        if obj:
            role_filter["actor"] = obj
        return Relatedactor.objects.filter(**role_filter).exists()


class SuperUserOnlyPermissions(LDPBasePermission):
    permissions = {"view", "add", "change", "delete"}

    def check_permission(self, user, model, obj):
        if user.is_superuser:
            return True

        return False

    def has_object_permission(self, request, view, obj=None):
        return self.check_permission(request.user, view.model, obj)
