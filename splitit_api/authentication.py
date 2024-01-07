from rest_framework.authentication import BaseAuthentication
import firebase_admin
from firebase_admin import credentials, auth
from django.conf import settings
from .models import Users

from .exceptions import NoAuthToken, InvalidAuthToken, FirebaseError

"""SETUP FIREBASE CREDENTIALS"""
cred = credentials.Certificate({
    "type": settings.FIREBASE_ACCOUNT_TYPE,
    "project_id": settings.FIREBASE_PROJECT_ID,
    "private_key_id": settings.FIREBASE_PRIVATE_KEY_ID,
    "private_key": settings.FIREBASE_PRIVATE_KEY.replace('\\n', '\n'),
    "client_email": settings.FIREBASE_CLIENT_EMAIL,
    "client_id": settings.FIREBASE_CLIENT_ID,
    "auth_uri": settings.FIREBASE_AUTH_URI,
    "token_uri": settings.FIREBASE_TOKEN_URI,
    "auth_provider_x509_cert_url": settings.FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
    "client_x509_cert_url": settings.FIREBASE_CLIENT_X509_CERT_URL
})
default_app = firebase_admin.initialize_app(cred)
"""FIREBASE AUTHENTICATION"""


def get_firebase_uid(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
    except Exception:
        raise InvalidAuthToken("Invalid auth token")
    """Return Nothing"""
    if not id_token or not decoded_token:
        return None
    """Get the uid of an user"""
    try:
        uid = decoded_token.get("uid")
    except Exception:
        raise FirebaseError()
    return uid


def get_firebase_user(uid):
    user = auth.get_user(uid)
    return {"id": user.uid, "email": user.email, "name": user.display_name}


class FirebaseAuthentication(BaseAuthentication):
    """override authenticate method and write our custom firebase authentication."""

    def authenticate(self, request):
        """Get the authorization Token, It raises exception when no authorization Token is given"""
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise NoAuthToken("No auth token provided")

        id_token = auth_header.split(" ").pop()
        uid = get_firebase_uid(id_token)

        user = Users.objects.get(pk=uid)
        return user
