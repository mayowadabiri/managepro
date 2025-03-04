from rest_framework.response import Response
from rest_framework import status


def api_response(success=True, message="", data=None, errors=None, http_status=status.HTTP_200_OK):
    """
    Centralized function to standardize API responses.
    """
    response_body = {
        "success": success,
        "message": message,
        "data": data if data else None,
        "errors": errors if errors else None
    }

    return Response(response_body, status=http_status)
