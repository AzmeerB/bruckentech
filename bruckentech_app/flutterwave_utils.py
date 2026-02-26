"""Flutterwave OAuth2 and API utilities."""

import time
import requests
from django.conf import settings

# Simple in-memory token cache
_token_cache = {
    'access_token': None,
    'expires_at': 0,
}


def get_flutterwave_access_token(force_refresh=False):
    """Fetch a Flutterwave OAuth2 access token, with caching.
    
    Args:
        force_refresh: If True, bypass cache and fetch a new token.
    
    Returns:
        The access token string.
    
    Raises:
        Exception: If the token request fails.
    """
    global _token_cache
    
    # Check if we have a valid cached token
    if not force_refresh and _token_cache['access_token']:
        if time.time() < _token_cache['expires_at']:
            return _token_cache['access_token']
    
    # Request a new token
    data = {
        'client_id': settings.FLUTTERWAVE_CLIENT_ID,
        'client_secret': settings.FLUTTERWAVE_CLIENT_SECRET,
        'grant_type': 'client_credentials',
    }
    
    response = requests.post(
        settings.FLUTTERWAVE_IDP_URL,
        data=data,
        timeout=10,
    )
    result = response.json()
    
    if response.status_code != 200:
        raise Exception(f"Failed to get Flutterwave access token: {result}")
    
    access_token = result.get('access_token')
    expires_in = result.get('expires_in', 3600)  # default 1 hour
    
    # Cache the token with expiry time (refresh 30s before expiry)
    _token_cache['access_token'] = access_token
    _token_cache['expires_at'] = time.time() + expires_in - 30
    
    return access_token
