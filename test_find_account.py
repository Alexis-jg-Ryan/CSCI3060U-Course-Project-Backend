import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import pytest
from backend.BackendSystem import BackendSystem #
from backend.Transaction import Transaction #


class TestFindAccount:

    @pytest.fixture(autouse=True)
    def setup(self):
        """initialize a BackendSystem instance and create test accounts before each test case"""
        self.backend = BackendSystem(
            master_accounts_path="backend/input/old_master_accounts.txt",
            merged_transactions_path="backend/input/merged_transactions.txt",
            output_current_path="backend/output/current_accounts.txt",
            output_master_path="backend/output/new_master_accounts.txt"
        )

        self.account_sp = {
            'account_number': '12345',
            'name': 'John Doe',
            'status': 'A',
            'balance': 1000.00,
            'total_transactions': 0,
            'plan': 'SP'
        }

        self.account_np = {
            'account_number': '54321',
            'name': 'Jane Smith',
            'status': 'A',
            'balance': 1500.00,
            'total_transactions': 0,
            'plan': 'NP'
        }

        self.backend.accounts = [self.account_sp, self.account_np]

    def test_tc1_none_input(self):
        # TC1 : Account_number is none - the if statement will then return a None output
        # note that this case covers the for loop never running.
        result = self.backend.find_account(None)
        assert result is None

    def test_tc2_empty_account_list(self):
        # pass a valid number, but the account list is empty
        # this case also covers the for loop never running
        self.backend.accounts = []
        result = self.backend.find_account(9999)
        self.backend.accounts = [self.account_sp, self.account_np] # set back to default after test
        assert result is None


    def test_tc3_account_exists(self):
        # pass a valid number, and ensure the account list has accounts
        # loop is run ONCE because this is the first account in the list
        result = self.backend.find_account(12345)
        assert result is not None
        assert result['account_number'] == '12345'

    def test_tc4_account_not_found(self):
        # pass a valid number, and ensure the account list has accounts
        # however, the valid number does not belong to an account in the account list
        # loop is run MULTIPLE TIMES because it will never find the account
        result = self.backend.find_account(9999)
        assert result is None


