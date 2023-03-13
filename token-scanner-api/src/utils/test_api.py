# -*- encoding: utf-8 -*-
# utils/test_api.py
# This class implements the tests for the API.

import src.utils.os_utils as os_utils

def _craft_url(env_vars, endpoint):
    """Craft the URL for the API."""

    host = env_vars['API_HOST_URL']
    if host == '0.0.0.0':
        host = 'http://localhost'
    port = env_vars['API_HOST_PORT']

    return f"{host}:{port}/{endpoint}"


def fetch_token_balance(env_vars, wallet):
    """Test the fetch_token_balance function."""
    
    endpoint = f'balance/{wallet}'

    url = _craft_url(env_vars, endpoint)
    
    response = os_utils.send_get_request(url)
    os_utils.log_info(response)


def fetch_top_token_holders(env_vars):
    """Test the fetch_top_token_holders function."""

    endpoint = f'top'

    url = _craft_url(env_vars, endpoint)
    
    response = os_utils.send_get_request(url)
    os_utils.log_info(response)


def fetch_change(env_vars, wallet):
    """Test the fetch_change function."""

    endpoint = f'weekly/{wallet}'

    url = _craft_url(env_vars, endpoint)
    
    response = os_utils.send_get_request(url)
    os_utils.log_info(response)
