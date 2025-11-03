from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


def get_request_info(request):
    """
    Extract all request information including headers, method, path, etc.
    """
    # Get all headers
    headers = {}
    for key, value in request.META.items():
        if key.startswith('HTTP_'):
            # Convert HTTP_HEADER_NAME to Header-Name format
            header_name = key[5:].replace('_', '-').title()
            headers[header_name] = value
        elif key in ['CONTENT_TYPE', 'CONTENT_LENGTH']:
            headers[key.replace('_', '-').title()] = value

    # Get query parameters
    query_params = dict(request.GET.items())

    # Get request body (for POST/PUT requests)
    body = None
    if hasattr(request, 'data') and request.data:
        body = request.data
    elif request.body:
        try:
            body = request.body.decode('utf-8')
        except UnicodeDecodeError:
            body = "<binary data>"

    return {
        "method": request.method,
        "path": request.path,
        "full_path": request.get_full_path(),
        "scheme": request.scheme,
        "headers": headers,
        "query_params": query_params,
        "body": body,
        "content_type": request.content_type,
        "user": {
            "is_authenticated": request.user.is_authenticated,
            "username": request.user.username if request.user.is_authenticated else None,
            "id": request.user.id if request.user.is_authenticated else None,
            "is_staff": request.user.is_staff if request.user.is_authenticated else None,
            "is_superuser": request.user.is_superuser if request.user.is_authenticated else None,
        },
        "remote_addr": request.META.get('REMOTE_ADDR'),
        "server_name": request.META.get('SERVER_NAME'),
        "server_port": request.META.get('SERVER_PORT'),
    }


@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
@permission_classes([AllowAny])
def unauthenticated_endpoint(request):
    """
    Unauthenticated endpoint that returns all request information.
    """
    request_info = get_request_info(request)
    request_info["endpoint"] = "unauthenticated"
    request_info["message"] = "This is the unauthenticated endpoint"

    return Response(request_info, status=status.HTTP_200_OK)


@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def authenticated_endpoint(request):
    """
    Authenticated endpoint that returns all request information.
    """
    request_info = get_request_info(request)
    request_info["endpoint"] = "authenticated"
    request_info["message"] = "This is the authenticated endpoint"

    return Response(request_info, status=status.HTTP_200_OK)


def get_all_settings():
    """
    Get all Django settings in a safe way.
    """
    import json
    from pathlib import Path

    settings_dict = {}

    # Get all settings from Django's settings object
    for setting_name in dir(settings):
        # Skip private/internal settings and methods
        if not setting_name.startswith('_') and setting_name.isupper():
            try:
                setting_value = getattr(settings, setting_name)

                # Convert non-serializable objects to strings
                if callable(setting_value):
                    settings_dict[setting_name] = f"<callable: {setting_value}>"
                elif isinstance(setting_value, Path):
                    settings_dict[setting_name] = str(setting_value)
                elif hasattr(setting_value, '__module__') and not isinstance(setting_value, (str, int, float, bool, list, dict, tuple)):
                    settings_dict[setting_name] = f"<object: {setting_value}>"
                else:
                    # Test if the value is JSON serializable
                    try:
                        json.dumps(setting_value)
                        settings_dict[setting_name] = setting_value
                    except (TypeError, ValueError):
                        settings_dict[setting_name] = str(setting_value)
            except Exception as e:
                settings_dict[setting_name] = f"<error accessing setting: {e}>"

    return settings_dict


@api_view(["GET"])
@permission_classes([AllowAny])  # We'll handle auth manually based on setting
def settings_endpoint(request):
    """
    Settings endpoint that returns all Django settings.
    Authentication requirement is configurable via MAIN_SETTINGS_ENDPOINT_REQUIRE_AUTH in main.settings.
    """
    # Check if authentication is required
    require_auth = getattr(settings, 'MAIN_SETTINGS_ENDPOINT_REQUIRE_AUTH', True)

    if require_auth and not request.user.is_authenticated:
        return Response(
            {
                "error": "Authentication required",
                "message": "This endpoint requires authentication. Set MAIN_SETTINGS_ENDPOINT_REQUIRE_AUTH=False in main.settings to make it public.",
                "authenticated": False,
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    all_settings = get_all_settings()

    response_data = {
        "endpoint": "settings",
        "message": "Django settings dump",
        "authentication_required": require_auth,
        "user": {
            "is_authenticated": request.user.is_authenticated,
            "username": request.user.username if request.user.is_authenticated else None,
        },
        "settings_count": len(all_settings),
        "settings": all_settings,
    }

    return Response(response_data, status=status.HTTP_200_OK)
