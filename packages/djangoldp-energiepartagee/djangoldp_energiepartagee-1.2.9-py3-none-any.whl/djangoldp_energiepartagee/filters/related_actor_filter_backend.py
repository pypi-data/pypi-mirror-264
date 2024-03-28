from rest_framework_guardian.filters import ObjectPermissionsFilter


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
            from djangoldp_energiepartagee.models.related_actor import Relatedactor

            user_actors_id = Relatedactor.get_user_actors_id(user=request.user)
            return queryset.filter(actor_id__in=user_actors_id)
