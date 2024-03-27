import base64
import os
import typing as t
import re

import requests
import extra_streamlit_components as stx
from .api.client import ApiClient

COOKIE_NAME = os.getenv('COOKIE_NAME', 'pollination-authz')
PROXY_URL = os.getenv('PROXY_URL', 'http://localhost:8000')
AUTH_PROXY_VERSION = os.getenv('AUTH_PROXY_VERSION', 'v0.5.5')

def get_manager():
    return stx.CookieManager()

def _auth_proxy_major_version() -> int:
    """Get the major version of app-auth-proxy

    Returns:
        int: The major version of app-auth-proxy
    """
    match = re.match(r'v?(\d+)\.\d+\.\d+', AUTH_PROXY_VERSION)
    if match:
        return int(match.group(1))
    else:
        raise ValueError(f"Invalid version: {AUTH_PROXY_VERSION}")

def get_api_client() -> ApiClient:
    """Get an authenticated API client

    Returns:
        ApiClient: An authenticated API client
    """

    client = ApiClient()

    if _auth_proxy_major_version() < 1:
        client.jwt_token = get_jwt()
    else:
        client.api_token = get_api_token()

    return client


def _decode_base64(data):
    """Decode base64, padding being optional.

    data: Base64 data as an ASCII byte string.
    """
    # Reference https://stackoverflow.com/a/53389061/4394669
    return base64.urlsafe_b64decode(data)


def _decrypt_cookie(cookie: str):
    b64_bytes = _decode_base64(str.encode(cookie))
    parts = b64_bytes.split(b'|')
    value = parts[1]
    token_bytes = _decode_base64(value)
    return token_bytes.decode('utf-8')


def _get_jwt_from_auth_proxy(cookie: str) -> str:
    """Get the logged in user JWT

    Returns:
    str: The base64 encoded user JWT
    """
    res = requests.get(
        f'{PROXY_URL}/auth/jwt',
        cookies={
            COOKIE_NAME: cookie
        }
    )
    res.raise_for_status()
    return res.text

def _get_api_token_from_auth_proxy(cookie: str) -> str:
    """Get the logged in user JWT

    Returns:
    str: The base64 encoded user JWT
    """
    res = requests.get(
        f'{PROXY_URL}/auth/api-token',
        cookies={
            COOKIE_NAME: cookie
        }
    )
    res.raise_for_status()
    return res.text

def get_jwt() -> t.Optional[str]:
    """Get and decrypt the logged in user's JWT

    Returns:
        t.Optional[str]: The decrypted auth cookie if it exists
    """
    cookies = get_manager().get_all()
    cookie = cookies.get(COOKIE_NAME)
    if cookie is None:
        return None
    try:
        return _get_jwt_from_auth_proxy(cookie)
    except requests.HTTPError:
        print(
            "Error fetching JWT from /auth/jwt endpoint. "
            "Defaulting to cookie decryption."
        )
        # Fallback to default cookie decryption technique if not using
        # app-auth-proxy > v0.5.0
        return _decrypt_cookie(cookie)


def get_api_token() -> t.Optional[str]:
    """Get and decrypt the logged in user's JWT

    Returns:
        t.Optional[str]: The decrypted auth cookie if it exists
    """
    cookies = get_manager().get_all()
    cookie = cookies.get(COOKIE_NAME)
    if cookie is None:
        return None
    return _get_api_token_from_auth_proxy(cookie)
