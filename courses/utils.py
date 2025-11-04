from requests import post
from django.conf import settings

def get_zoom_access_token():
    url = "https://zoom.us/oauth/token"
    response = post(
        url,
        params={
            "grant_type": "account_credentials",
            "account_id": settings.ZOOM_ACCOUNT_ID,
        },
        auth=(settings.ZOOM_CLIENT_ID, settings.ZOOM_CLIENT_SECRET)
    )

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Ошибка при получении токена Zoom: {response.text}")