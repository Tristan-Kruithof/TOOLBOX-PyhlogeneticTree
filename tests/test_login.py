import sys
sys.path.append('..')
from python.login import Account
from unittest.mock import patch
import pytest


# Tests for login.py
# Tests if it returns false when it goes over 10 runs
def test_fake_load_over_limit():
    acc = Account("test@example.com")

    def fake_load():
        acc.accounts = [{"email": "test@example.com", "runs": 10, "admin": False, "newsletter": False, "trees": {}}]
        acc.account = acc.accounts[0]

    with patch.object(acc, "load_accounts", fake_load):
        acc.signin()

    assert acc.status[0] is False


# Testing login in as admin but with too many runs
def test_signin_admin_bypass():
    acc = Account("test@example.com")

    def fake_load():
        acc.accounts = [{"email": "test@example.com", "runs": 99, "admin": True, "newsletter": False, "trees": {}}]
        acc.account = acc.accounts[0]

    with patch.object(acc, "load_accounts", fake_load):
        acc.signin()

    assert acc.status[0] is True


# Testing add_run
def test_add_run_increments():
    acc = Account("test@example.com")
    fake_data = {"email": "test@example.com", "runs": 2, "admin": False, "newsletter": False, "trees": {}}

    def fake_load():
        acc.accounts = [fake_data]
        acc.account = fake_data

    with patch.object(acc, "load_accounts", fake_load):
        with patch.object(acc, "save_accounts", lambda: None):
            acc.add_run()

    assert acc.status[0] is True
    assert fake_data["runs"] == 3