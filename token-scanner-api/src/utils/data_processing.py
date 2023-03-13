# -*- encoding: utf-8 -*-
# utils/data_processing.py
# Data processing for token transfers.

import collections
from decimal import Decimal

import src.utils.os_utils as os_utils


def process_balances(filepath) -> list:
    """Return a list of balances for each address."""

    data = os_utils.open_json(filepath)
    balances = collections.defaultdict(Decimal)

    for _tx, event_data in data.items():
        balances[event_data["from"]] -= Decimal(event_data["amount"])
        balances[event_data["to"]] += Decimal(event_data["amount"])


    balances = {key: float(value) for key, value in balances.items() if value > Decimal('0')}
    return dict(sorted(balances.items(), key=lambda x: x[1]))


def run_data_processing(filepath) -> None:
    """Run data processing."""

    balance_data = process_balances(filepath)
    balance_output_file = os_utils.create_result_file("balances")
    balance_output_filepath = os_utils.set_output(balance_output_file)

    os_utils.log_info(f'Writing balances to {balance_output_filepath}')
    os_utils.save_output(balance_output_filepath, balance_data)
