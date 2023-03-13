# -*- encoding: utf-8 -*-
# utils/test_api.py
# This class implements the tests for the API.

import src.utils.os_utils as os_utils


def fetch_token_balance(ewallet):
    """Test the fetch_token_balance function."""
    
    endpoint = f"balance/{wallet}"
    url = f'http://localhost:80/{endpoint}'
    response = os_utils.send_get_request(url)
    os_utils.log_info(response)


def fetch_top_token_holders(env_vars, top_number):
    """Test the fetch_top_token_holders function."""

    url = os_utils.format_url(f"{env_vars['API_HOST_URL']}:{env_vars['API_HOST_PORT']}", \
                              "top")
    response = os_utils.send_get_request(url)
    os_utils.log_info(response)


def fetch_change(env_vars, wallet):
    """Test the fetch_change function."""

    url = os_utils.format_url(f"{env_vars['API_HOST_URL']}:{env_vars['API_HOST_PORT']}", \
                              f"/weekly/{wallet}")
    response = os_utils.send_get_request(url)
    os_utils.log_info(response)
