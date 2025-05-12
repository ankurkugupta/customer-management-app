

import json
from rest_framework.renderers import JSONRenderer




class CustomJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):

        response_data = {
            "status": "Success",
            "message": "",
            "errors": [],
            "data": None
        }
        response = renderer_context.get('response', None)

        if renderer_context:
            view = renderer_context.get('view')
            if hasattr(view, 'custom_message'):
                response_data["message"] = view.custom_message
            else:
                if response.status_code >=500:
                    response_data["message"] = "Internal Server Error"
                elif response.status_code>=400:
                    response_data["message"] = "Bad Request"
                elif response.status_code>=200:
                    response_data["message"] = "Success"

        if not data and 200 <= response.status_code < 400:
            return super().render(response_data, accepted_media_type, renderer_context)

        if isinstance(data, dict) and list(data.keys())==list(response_data.keys()):
            return super().render(data, accepted_media_type, renderer_context)

        # If errors exist
        if response and response.status_code >= 400:
            response_data["status"] = "Failure"
            response_data["errors"] = data
        else:
            response_data["data"] = data

        # Allow API views to pass custom messages


        if data:
            if "message" in data :
                response_data["message"] = data["message"]

            if "detail" in data:
                response_data["errors"] = data["detail"]

            if "messages" in data:
                response_data["errors"] = data["messages"]

        return super().render(response_data, accepted_media_type, renderer_context)