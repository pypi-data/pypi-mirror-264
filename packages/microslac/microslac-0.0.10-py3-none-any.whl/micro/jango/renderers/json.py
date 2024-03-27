from rest_framework import status
from rest_framework.renderers import JSONRenderer


class ResponseRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        omit_view_sets = set()

        if renderer_context:
            view = renderer_context.get("view")
            response = renderer_context.get("response")
            if response and view.basename not in omit_view_sets:
                if response.data is None:
                    response.data = data = {}
                if isinstance(data, dict):
                    if status.is_success(response.status_code):
                        data.setdefault("ok", True)
                    if status.is_client_error(response.status_code):
                        data.setdefault("ok", False)
                    if status.is_server_error(response.status_code):
                        data.setdefault("ok", False)
        return super().render(data, accepted_media_type, renderer_context)
