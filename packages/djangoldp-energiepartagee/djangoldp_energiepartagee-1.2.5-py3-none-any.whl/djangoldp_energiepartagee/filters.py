from rest_framework_guardian.filters import ObjectPermissionsFilter
from djangoldp.utils import is_anonymous_user

#######
# Returns the contributions of the actors the user is admin of (through related actors)
# Or all the contributions if the user is superuser
#######
class ContributionFilterBackend(ObjectPermissionsFilter):
    def filter_queryset(self, request, queryset, view):
        if not request.user.is_authenticated or request.user.is_anonymous:
            return queryset.none()
        elif request.user.is_superuser:
            return queryset
        else:
            from .models import Relatedactor
            user_actors_id = Relatedactor.get_user_actors_id(user=request.user, role='admin')
            return queryset.filter(actor_id__in=user_actors_id)

#######
# Returns the related actors on which the user is admin
# Or the complete list if the user is superuser
#######
class RelatedactorFilterBackend(ObjectPermissionsFilter):
    def filter_queryset(self, request, queryset, view):
        if not request.user.is_authenticated or request.user.is_anonymous:
            return queryset.none()
        elif request.user.is_superuser:
            return queryset
        else:
            from .models import Relatedactor
            user_actors_id = Relatedactor.get_user_actors_id(user=request.user)
            return queryset.filter(actor_id__in=user_actors_id)