import json

import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http.response import JsonResponse
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

try:
    INSTAGRAM_APP_ID = getattr(settings, "INSTAGRAM_APP_ID", "")
except AttributeError:
    raise ImproperlyConfigured("INSTAGRAM_APP_ID is required in settings.")

try:
    INSTAGRAM_SECRET = getattr(settings, "INSTAGRAM_SECRET", "")
except AttributeError:
    raise ImproperlyConfigured("INSTAGRAM_SECRET is required in settings.")


@csrf_exempt
@require_http_methods(["POST"])
def ig_token(request):
    if not settings.DEBUG:
        raise Http404("Page not found")

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(status=400, data={
            "errorCode": "badFormed",
        })

    if not data.get("code", None):
        return JsonResponse(status=400, data={
            "error": "No code supplied",
            "errorCode": "noToken",
        })

    if not data.get("uri", None):
        return JsonResponse(status=400, data={
            "error": "No redirect Uri supplied",
            "errorCode": "noRedirectUri",
        })

    ig_data = {
        "code": data.get("code"),
        "redirect_uri": data.get("uri"),
        "grant_type": "authorization_code",
        "client_id": INSTAGRAM_APP_ID,
        "client_secret": INSTAGRAM_SECRET
    }

    result = requests.post("https://api.instagram.com/oauth/access_token", ig_data)
    returned_data = result.json()

    return JsonResponse(status=result.status_code, data=returned_data)
