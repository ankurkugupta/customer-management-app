import json

from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response

import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)

    if isinstance(exc,ValidationError):
        # handle validation error raised from the service, repository
        if exc.messages:
            is_string=True
            for message in exc.messages:
                if not isinstance(message,str):
                    is_string=False
                    break
            if is_string:
                logger.info(f"Error {" ".join(exc.messages)}")
                return Response({"status":"Failure","message":" ".join(exc.messages),"errors":[],"data":None},status=status.HTTP_400_BAD_REQUEST)
            logger.info(f"Error {json.dumps(exc.messages)}")
            return Response({"status":"Failure","message":"Validation Errors","errors":exc.messages,"data":None},status=status.HTTP_400_BAD_REQUEST)

    if response is not None:
        # Let standard DRF error responses pass through
        return response

    logger.error("Unhandled exception", exc_info=exc)


    # Handle unknown exceptions (500 errors, etc.)
    return Response({
        "status": "Failure",
        "message": "An unexpected error occurred.",
        "errors": str(exc),
        "data": None
    }, status=500)
