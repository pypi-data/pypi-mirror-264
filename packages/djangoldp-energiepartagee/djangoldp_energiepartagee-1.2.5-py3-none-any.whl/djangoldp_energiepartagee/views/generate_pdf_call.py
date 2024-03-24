import validators

from django.http import HttpResponse
from django.views.generic.detail import DetailView

from djangoldp.models import Model

from djangoldp_energiepartagee.models.contribution import Contribution
from djangoldp_energiepartagee.views.utils import render_to_pdf


class GeneratePdfCall(DetailView):
    model = Contribution
    template_name = "pdf/contribution_call.html"

    def get(self, request, *args, **kwargs):
        # try:
        #     from djangoldp_energiepartagee.models import Contribution
        # except (get_user_model().DoesNotExist, KeyError):
        #     pass

        instance = Contribution.objects.get(id=kwargs["pk"])
        # Check that the array entries are URLs
        if instance:
            context = {
                "contribution": instance,
                "uri": request.build_absolute_uri("/media/"),
            }
            pdf = render_to_pdf(self.template_name, context)

            if pdf:
                response = HttpResponse(
                    pdf, content_type="application/pdf; charset=utf-8"
                )
                filename = "Appel à cotisation.pdf"
                content = "inline; filename=%s" % (filename)
                response["Content-Disposition"] = content
                return response

        return HttpResponse("Not Found")

    def post(self, request, *args, **kwargs):
        # try:
        #     from djangoldp_energiepartagee.models import Contribution
        # except (get_user_model().DoesNotExist, KeyError):
        #     pass

        # Check that the array entries are URLs
        if validators.url(request.data.urlid):
            # Check that the corresponding Actors exists
            model, instance = Model.resolve(request.data.urlid)

            context = {
                "number": instance.contributionnumber,
                "actor": instance.actor.name,
            }
            pdf = render_to_pdf(self.template_name, context)

            if pdf:
                response = HttpResponse(
                    pdf, content_type="application/pdf; charset=utf-8"
                )
                filename = "Appel à cotisation.pdf"
                content = "inline; filename=%s" % (filename)
                response["Content-Disposition"] = content
                return response

        return HttpResponse("Not Found")
