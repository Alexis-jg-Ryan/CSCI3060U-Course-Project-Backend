from enum import nonmember

from Transaction import Transaction
from read import read_old_bank_accounts, read_transactions
from write import write_new_current_accounts, write_new_master_accounts
from print_error import log_constraint_error

class BackendSystem:
    def __init__(self, master_accounts_path, merged_transactions_path, output_current_path, output_master_path):
        self.master_accounts_path = master_accounts_path
        self.merged_transactions_path = merged_transactions_path
        self.output_current_path = output_current_path
        self.output_master_path = output_master_path

        # list of account dictionary
        self.accounts = []

    '''
    Run the full backend system
    '''
    def run(self):
        self.load_accounts()
        self.process_transactions()
        self.write_output_files()

    '''
    Loads accounts from old master accounts file.
    Format: NNNNN AAAAAAAAAAAAAAAAAAAA S PPPPPPPP TTTT PP (45 characters)
    '''
    def load_accounts(self):
        self.accounts = read_old_bank_accounts(self.master_accounts_path)

    '''
    Return the account dictionary matching account_number
    '''
    def find_account(self, account_number):
        target = str(int(account_number))
        for account in self.accounts:
            if str(int(account['account_number'])) == target:
                return account
        return None

    '''
    Read all transactions from the merged file and apply each one
    '''
    def process_transactions(self):
        transactions = read_transactions(self.merged_transactions_path)
        for transaction in transactions:
            self.process_transaction(transaction)

    '''
    match transaction to the respective apply_method.
    '''
    def process_transaction(self, transaction):
        code = transaction.code

        # end_session
        if code == "00":
            return

        dispatch = {
            "01": self.apply_withdrawal,
            "02": self.apply_transfer,
            "03": self.apply_paybill,
            "04": self.apply_deposit,
            "05": self.apply_create,
            "06": self.apply_delete,
            "07": self.apply_disable,
            "08": self.apply_changeplan,
        }

        handler = dispatch.get(code)
        if handler is None:
            log_constraint_error(
                f"Unknown transaction code '{code}' – transaction skipped: {transaction}",
                "Unknown transaction code"
            )
            return

        handler(transaction)

    """
    Debit the per-transaction fee and increment the transaction counter.
    Student plan (SP): $0.05
    Non-student plan (NP): $0.10
    """
    def charge_transaction_fee(self, account):

        fee = 0.05 if account['plan'] == 'SP' else 0.10
        new_balance = round(account['balance'] - fee, 2)

        if new_balance < 0.0:
            log_constraint_error(
                f"Account {account['account_number']!r} balance ({account['balance']:.2f}) "
                f"is insufficient to cover transaction fee ({fee:.2f}). Fee not charged.",
                "TRANSACTION FEE: insufficient funds"
            )
        else:
            account['balance'] = new_balance

        account['total_transactions'] += 1

    '''
    Add the deposited amount to the account balance, deduct fee.
    '''
    def apply_deposit(self, t):
        account = self.find_account(t.account_num)

        account['balance'] = round(account['balance'] + t.amount, 2)
        self.charge_transaction_fee(account)

    '''
    Subtract the transaction amount from the account balance, deduct fee.
    '''
    def apply_withdrawal(self, t):
        account = self.find_account(t.account_num)

        new_balance = round(account['balance'] - t.amount, 2)
        # constraint: account balance must be at least $0.00 after withdrawal
        if new_balance < 0.0:
            log_constraint_error(
                f"Account {t.account_num!r} would go negative "
                f"(balance={account['balance']:.2f}, withdrawal={t.amount:.2f})",
                "WITHDRAWAL: insufficient funds"
            )
            return

        account['balance'] = new_balance
        self.charge_transaction_fee(account)

    '''
    Transfer amount from sender to receiver account, deduct fee.
    '''
    def apply_transfer(self, t):
        sender = self.find_account(t.account_num)
        receiver = self.find_account(t.misc)

        new_sender_balance = round(sender['balance'] - t.amount, 2)
        # constraint: sender balance must be at least $0.00 after transfer
        if new_sender_balance < 0.0:
            log_constraint_error(
                f"Sender account {t.account_num!r} would go negative "
                f"(balance={sender['balance']:.2f}, transfer={t.amount:.2f})",
                "TRANSFER: insufficient funds"
            )
            return

        sender['balance'] = new_sender_balance
        receiver['balance'] = round(receiver['balance'] + t.amount, 2)
        self.charge_transaction_fee(sender)

    '''
    Pay a bill from the account, deduct fee.
    '''
    def apply_paybill(self, t):
        account = self.find_account(t.account_num)

        new_balance = round(account['balance'] - t.amount, 2)
        # constraint: no negative balances allowed
        if new_balance < 0.0:
            log_constraint_error(
                f"Account {t.account_num!r} would go negative "
                f"(balance={account['balance']:.2f}, payment={t.amount:.2f})",
                "PAYBILL: insufficient funds"
            )
            return

        account['balance'] = new_balance
        self.charge_transaction_fee(account)

    '''
    Create a new bank account with the given number, name, and initial balance.
    '''
    def apply_create(self, t):
        new_account = {
            'account_number': str(int(t.account_num)),  # strip leading zeros
            'name': t.name.strip()[:20],
            'status': 'A',
            'balance': round(t.amount, 2),
            'total_transactions': 0,
            'plan': 'SP',  # new accounts default to student plan
        }
        self.accounts.append(new_account)
        self.accounts.sort(key=lambda a: a['account_number'].zfill(5))

    '''
    Remove a bank account from the system.
    '''
    def apply_delete(self, t):
        account = self.find_account(t.account_num)
        self.accounts.remove(account)

    '''
    Change status from active (A) to disabled (D).
    '''
    def apply_disable(self, t):
        account = self.find_account(t.account_num)

        account['status'] = 'D'
        self.charge_transaction_fee(account)

    '''
    Change the transaction payment plan for an account.
    '''
    def apply_changeplan(self, t):
        account = self.find_account(t.account_num)

        new_plan = t.misc.strip().upper()
        if new_plan not in ('SP', 'NP'):
            # Toggle if the misc field doesn't carry a valid plan code
            new_plan = 'NP' if account['plan'] == 'SP' else 'SP'

        account['plan'] = new_plan
        self.charge_transaction_fee(account)

    '''
    Write both output files from the current in-memory account list.
    '''
    def write_output_files(self):
        write_new_current_accounts(self.accounts, self.output_current_path)
        write_new_master_accounts(self.accounts, self.output_master_path)
