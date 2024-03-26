from django.http import HttpResponseNotFound, HttpResponseServerError
from rest_framework import status


class ApiMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == status.HTTP_404_NOT_FOUND:
            return HttpResponseNotFound({"error": "not_found"})
        elif response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            return HttpResponseServerError({"error": "server_error"})

        return response
