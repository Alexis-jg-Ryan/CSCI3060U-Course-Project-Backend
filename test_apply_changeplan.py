"""
Unit Tests for BackendSystem.apply_changeplan() method with Statement Coverage - 4 test cases covering all statements in each of the method for validity.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import pytest
from backend.BackendSystem import BackendSystem #
from backend.Transaction import Transaction #


class TestApplyChangePlan:
    
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
    
    def test_tc1_valid_plan_code(self):
        """
        TC1: Valid plan code 'SP'
        covers statements 1, 2, 3, 5, 6
        """
        transaction = Transaction(
            code='08', name='John Doe', account_num=12345, 
            amount=0.00, misc='SP'
        )
        initial_balance = self.account_sp['balance']
        
        self.backend.apply_changeplan(transaction)
        
        assert self.account_sp['plan'] == 'SP'
        assert self.account_sp['balance'] == round(initial_balance - 0.05, 2)
    
    def test_tc2_invalid_plan_sp_toggles_to_np(self):
        """
        TC2: Invalid plan 'XX' with account SP 
        covers statements 1, 2, 3, 4, 5, 6
        """
        transaction = Transaction(
            code='08', name='John Doe', account_num=12345, 
            amount=0.00, misc='XX'
        )
        initial_balance = self.account_sp['balance']
        
        self.backend.apply_changeplan(transaction)
        
        assert self.account_sp['plan'] == 'NP'
        assert self.account_sp['balance'] == round(initial_balance - 0.10, 2)
    
    def test_tc3_invalid_plan_np_toggles_to_sp(self):
        """
        TC3: Invalid plan 'XX' with account NP 
        covers statements 1, 2, 3, 4, 5, 6
        """
        transaction = Transaction(
            code='08', name='Jane Smith', account_num=54321, 
            amount=0.00, misc='XX'
        )
        initial_balance = self.account_np['balance']
        
        self.backend.apply_changeplan(transaction)
        
        assert self.account_np['plan'] == 'SP'
        assert self.account_np['balance'] == round(initial_balance - 0.05, 2)

    def test_tc4_missing_account_should_not_crash(self):
        """
        TC4: failure case when account number does not exist.
        TypeError due to account being None.
        """
        transaction = Transaction(
            code='08', name='Ghost User', account_num=99999,
            amount=0.00, misc='NP'
        )

        self.backend.apply_changeplan(transaction)
