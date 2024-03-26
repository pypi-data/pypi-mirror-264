from django.http import HttpResponseNotFound, HttpResponseServerError
from django.utils.translation import gettext_lazy as _
from rest_framework import status


class ApiMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == status.HTTP_404_NOT_FOUND:
            return HttpResponseNotFound( _("HTTP response 404 not found."))
        elif response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            return HttpResponseServerError(_("HTTP response 500 internal server error."))

        return response
