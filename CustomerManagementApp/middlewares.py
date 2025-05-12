import json
import logging
import uuid
from threading import current_thread

from django.utils import timezone

logger = logging.getLogger(__name__)


class RequestIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = str(uuid.uuid4())
        request.request_id = request_id

        current_thread().request = request  # Bind request to current thread
        start_time=timezone.now()
        if request.body and "password" not in str(request.body):
            logger.info(f"request_body {str(request.body)}")
        response = self.get_response(request)
        response["X-Request-ID"] = request_id
        end_time=timezone.now()
        logger.info(f"response_time-{end_time-start_time}")
        return response
