from djangoldp.utils import is_authenticated_user
from djangoldp.permissions import LDPBasePermission
from djangoldp_energiepartagee.filters import *

class ContributionPermissions(LDPBasePermission):
    filter_backend = ContributionFilterBackend
    permissions = {'view'}

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
        if request.user and request.user.is_authenticated:
            admin_actor_pks = Relatedactor.get_mine(user=request.user, role='admin').values_list('pk', flat=True)
            member_actor_pks = Relatedactor.get_mine(user=request.user, role='membre').values_list('pk', flat=True)

            if obj.actor.pk in admin_actor_pks:
                return request.method in ['GET', 'PUT', 'PATCH']  # Admins can view, change
            elif obj.actor.pk in member_actor_pks:
                return request.method == 'GET'  # Members can view

        return False

####
# Only the admin of an actor can modify it (and superusers of course)
# Members can view the actor
####
class ActorPermissions(LDPBasePermission):
    permissions = {'add'}

    def get_permissions(self, user, model, obj=None):
        if user.is_anonymous:
            return {}

        '''returns the permissions the user has on a given model or on a given object'''
        perms = super().get_permissions(user, model, obj)
        if user.is_superuser:
            return perms.union({'view', 'add', 'change', 'delete'})

        if obj and self.is_admin(user, obj):
          return perms.union({'view', 'add', 'change', 'delete'})

        if obj and self.is_member_or_admin(user, obj):
          return perms.union({'view', 'add'})

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
        from .models import Relatedactor
        """Check if the user is a member or admin. If obj is provided, check is specific to that object."""
        role_filter = {'user': user, 'role__in': ['membre', 'admin']}
        if obj:
            role_filter['actor'] = obj
        return Relatedactor.objects.filter(**role_filter).exists()

    def is_admin(self, user, obj=None):
        from .models import Relatedactor
        """Check if the user is an admin. If obj is provided, check is specific to that object."""
        role_filter = {'user': user, 'role': 'admin'}
        if obj:
            role_filter['actor'] = obj
        return Relatedactor.objects.filter(**role_filter).exists()

class SuperUserOnlyPermissions(LDPBasePermission):
    permissions = {'view', 'add', 'change', 'delete'}

    def check_permission(self, user, model, obj):
        if user.is_superuser:
            return True

        return False

    def has_object_permission(self, request, view, obj=None):
        return self.check_permission(request.user, view.model, obj)

####
# Only the admin of an actor can modify it (and superusers of course)
# Members can view the actor
####
class RelatedactorPermissions(LDPBasePermission):
    permissions = {'view', 'add', 'change', 'delete'}

    filter_backend = RelatedactorFilterBackend

    def get_filter_backend(cls, model):
        return cls.filter_backend

    def has_permission(self, request, view):
        if request.method == "OPTIONS":
            return True
        if request.user.is_anonymous:
            return False
        from .models import Relatedactor
        # Allow container-level 'add' action for authenticated users.        
        if request.method == 'POST':
            role = request.data.get('role')
            if role in ('admin', 'membre', 'refused'):
              actor_urlid = request.data.get('actor')['@id']
              if actor_urlid:
                  return Relatedactor.objects.filter(actor__urlid=actor_urlid, user=request.user, role__in=('admin', 'membre')).exists()
              return False  # If no actor ID is provided, deny permission
            elif role is None and request.user.is_authenticated:
              return True

        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj=None):
        if request.method == "OPTIONS":
            return True
        if request.user.is_anonymous:
            return False
        from .models import Relatedactor
        # Call super to keep default LDPBasePermission checks
        if not super().has_object_permission(request, view, obj):
            return False
        
        # Direct permission if the user is the same as the object's user
        if request.user == obj.user:
            if obj.role == 'admin':
                return request.method in ['GET', 'PUT', 'PATCH', 'DELETE', 'POST']
            elif obj.role == 'membre' or obj.role is None or obj.role == '':
                return request.method == 'GET'

        # Additional checks for admin/member roles related to the actor
        if hasattr(obj, 'actor') and obj.actor is not None:
            user_actors_ids = Relatedactor.get_user_actors_id(user=request.user, role='admin')
            if obj.actor.id in user_actors_ids:
                return request.method in ['GET', 'PUT', 'PATCH', 'DELETE', 'POST']

        #     user_actors_ids = Relatedactor.get_user_actors_id(user=request.user)
        #     if obj.actor.id in user_actors_ids:
        #         return request.method == 'GET'

        # Default to False if none of the above conditions are met
        return False