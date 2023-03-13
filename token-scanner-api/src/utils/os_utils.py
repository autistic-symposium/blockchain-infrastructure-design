# -*- encoding: utf-8 -*-
# utils/os.py
# This class implements OS/file system util methods used by the other classes.

import os
import sys
import json
import logging
import requests
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
from urllib.parse import urlparse


def set_logging(log_level) -> None:
    """Set logging level according to .env config."""

    if log_level == 'info':
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    elif log_level == 'error':
        logging.basicConfig(level=logging.ERROR, format='%(message)s')

    elif log_level == 'debug':
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')

    else:
        print(f'Logging level {log_level} is not available. Setting to ERROR')
        logging.basicConfig(level=logging.ERROR, format='%(message)s')


def load_config() -> dict:
    """Load and set environment variables."""

    env_file = Path('.') / '.env'
    if not os.path.isfile(env_file):
        exit_with_error('Please create an .env file')

    env_vars = {}
    load_dotenv(env_file)

    try:
        env_vars['RPC_PROVIDER_URL'] = os.getenv("RPC_PROVIDER_URL")
        env_vars['TOKEN_CONTRACT'] = os.getenv("TOKEN_CONTRACT")
        env_vars['TOKEN_CONTRACT_ABI'] = os.getenv("TOKEN_CONTRACT_ABI")
        env_vars['MAX_RETRIES'] = os.getenv("MAX_RETRIES")           
        env_vars['SIZE_CHUNK_NEXT'] = os.getenv("SIZE_CHUNK_NEXT")           
        env_vars['OUTPUT_DIR'] = os.getenv("OUTPUT_DIR") 
        env_vars['TOKEN_DECIMALS'] = os.getenv("TOKEN_DECIMALS")
        env_vars['MONGODB_URL'] = os.getenv("MONGODB_URI")
        env_vars['MONGODB_DB_NAME'] = os.getenv("MONGODB_DB_NAME") 
        env_vars['MONGODB_COLLECTION_NAME'] = os.getenv("MONGODB_COLLECTION_NAME")     
        env_vars['API_HOST_URL'] = os.getenv("API_HOST_URL")
        env_vars['API_HOST_PORT'] = os.getenv("API_HOST_PORT")
        set_logging(os.getenv("LOG_LEVEL"))
        return env_vars

    except KeyError as e:
        exit_with_error(f'Cannot extract env variables: {e}. Exiting.')


def log_error(string) -> None:
    """Print STDOUT error using the logging library."""

    logging.error('⛔️ %s', string)


def log_info(string) -> None:
    """Print STDOUT info using the logging library."""

    logging.info('ℹ️ %s', string)


def log_debug(string) -> None:
    """Print STDOUT debug using the logging library."""

    logging.debug('⚠️ %s', string)


def open_json(filepath) -> dict:
    """Load and parse a file."""

    try:
        with open(filepath, 'r', encoding='utf-8') as infile:
            return json.load(infile)

    except (IOError, FileNotFoundError, TypeError) as e:
        exit_with_error(f'Failed to parse: "{filepath}": {e}')


def format_path(dir_path, filename) -> str:
    """Format a OS full filepath."""

    return os.path.join(dir_path, filename)


def format_url(base_url, endpoint) -> str:
    """Format a URL full filepath."""

    return urlparse.urljoin(base_url, endpoint)


def save_output(destination, data, mode="w") -> None:
    """Save data from memory to a destination in disk."""

    try:
        with open(destination, mode, encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=4)
            log_info(f'Results were saved at {destination}.')

    except (IOError, TypeError) as e:
        log_error(f'Could not save {destination}: {e}')


def create_dir(result_dir) -> None:
    """Check whether a directory exists and create it if needed."""

    try:
        if not os.path.isdir(result_dir):
            os.mkdir(result_dir)

    except OSError as e:
        log_error(f'Could not create {result_dir}: {e}')


def set_output(output_file, env_vars=None) -> str:
    """Create an output destination to save solutions."""

    if env_vars is None:
        env_vars = load_config()

    try:
        output_dir = env_vars['OUTPUT_DIR']
        create_dir(output_dir)
        return format_path(output_dir, output_file)

    except (TypeError, KeyError) as e:
        exit_with_error(f'Could not format output file: {e}')


def exit_with_error(message) -> None:
    """Log an error message and halt the program."""
    log_error(message)
    sys.exit(1)


def create_result_file(prefix) -> str:
    """Create an output file to save solutions."""

    this_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f'{prefix}_{this_time}.json'


def send_post_request(url, headers=None, json=None) -> dict:
    """Send a request to a given URL"""

    json = json or {}
    headers = headers or {}

    try:
        response = requests.post(url, headers=headers, json=json)
        return response.json()

    except requests.exceptions.HTTPError  as e:
        log_error('Error querying to {0}: {1}'.format(url, e.response.text))    

    return {}


def send_get_request(url, params=None) -> dict:
    """Send a request to a given URL"""

    params = params or {}

    try:
        response = requests.get(url, params=params)
        return response.json()

    except requests.exceptions.HTTPError  as e:
        log_error('Error querying to {0}: {1}'.format(url, e.response.text))    

    return {}


def send_rpc_request(url, method, params=None) -> dict:
    """Send a JSON-RPC request to a given URL"""
    
    params = params or []
    data = {'jsonrpc': '2.0', 'method': method, 'params': params, 'id': 1}
    log_debug(f'Querying {url} with {data}')

    response = send_post_request(url, headers={'Content-Type': 'application/json'}, json=data)
    if 'result' in response:
        return response['result']
    else:
        log_error('Query failed: {}.'.format(response.json()['error']))

