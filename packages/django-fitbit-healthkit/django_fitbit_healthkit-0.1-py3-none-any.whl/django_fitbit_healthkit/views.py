import urllib
import requests
from base64 import b64encode

from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, Http404

from main import settings
from .models import FitbitUser


def login(request: HttpRequest) -> HttpResponseRedirect:
    '''
    Redirect to authenticate to with Fitbit.
    '''
    data = {
        "client_id": settings.FITBIT_CLIENT_ID,
        "redirect_uri": settings.FITBIT_CALLBACK_URL,
        "response_type": "code",
        "scope": "activity heartrate location nutrition profile settings sleep social weight",
        "expires_in": 604800
    }
    if settings.DEBUG:
        data["redirect_uri"] = "http://localhost:8000/fitbit/success"
    return HttpResponseRedirect(
        settings.FITBIT_AUTHORIZATION_URI + "?" + urllib.parse.urlencode(data)
    )


def success(request: HttpRequest) -> HttpResponse:
    if "code" not in request.GET:
        return Http404(f"No access code returned: {request.GET}.")

    data = {
        # maybe an error, but the docs here say client_id:
        # https://dev.fitbit.com/build/reference/web-api/oauth2/
        # though, above it doesn't say it's required
        # but the tool uses clientId:
        # https://dev.fitbit.com/apps/oauthinteractivetutorial
        "client_id": settings.FITBIT_CLIENT_ID,
        "code": request.GET["code"],
        "grant_type": "authorization_code",
        "redirect_uri": settings.FITBIT_CALLBACK_URL,
    }
    if settings.DEBUG:
        data["redirect_uri"] = "http://localhost:8000/fitbit/success"
    encoded = b64encode(
        "{client_id}:{client_secret}".format(
            client_id=settings.FITBIT_CLIENT_ID, client_secret=settings.FITBIT_CLIENT_SECRET
        ).encode("latin1")
    )
    content = "Basic {encoded}".format(encoded=encoded.decode("latin1"))
    headers = {'Authorization': content}
    r = requests.post(
        settings.FITBIT_ACCESS_REFRESH_TOKEN_REQUEST_URI,
        data=data,
        headers=headers
    )
    # rather than raise an application error, pass that error back to the user:
    # r.raise_for_status()
    if r.status_code != requests.codes.ok:
        raise Http404(f"Error in fitbit oauth handshake: {r.text}")

    fitbit_user = r.json()
    if "access_token" not in fitbit_user:
        raise Http404(f"No access token returned response: {fitbit_user}.")

    if settings.DEBUG:
        print(fitbit_user)

    # update the token too
    (fb_user, created) = FitbitUser.objects.get_or_create(user=request.user)
    fb_user.access_token = fitbit_user.get("access_token")
    fb_user.refresh_token = fitbit_user.get("refresh_token")
    fb_user.expires_in = fitbit_user.get("expires_in")
    fb_user.fitbit_id = fitbit_user.get("user_id")
    fb_user.save()

    # get_athlete_activities(ath, max_requests=1)
    # t = threading.Thread(target=get_user_data, args=[s, 100])
    # t.setDaemon(True)
    # t.start()

    return render(request, "fitbit/success.html", fitbit_user)