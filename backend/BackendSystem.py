# To be created

# The Back End reads the Master Bank Accounts File (see below) and the Merged
# Bank Account Transaction File (see below) and applies all transactions to the Old
# Master Bank Accounts File to produce the New Master Bank Accounts File and
# the new Current Bank Accounts File.
# The Back End also calculates the daily cost of transaction based on the account
# plan. If the account plan is a student plan the account is debited $0.05 for each
# transaction. If the account plan is a non-student plan, the account is debited
# $0.10 for each transaction.
# The Back End enforces the following business constraints, and produces a failed
# constraint log on the terminal as it processes transactions from the merged back
# account transaction file.
# Constraints:
# • no bank account should ever have a negative balance
# • a newly created bank account must have an account number different
# from all existing bank accounts


class BackendSystem:
    def __init__(self, input_folder, output_folder):
        self.merged_transactions_txt = f"{input_folder}/merged_transactions.txt"
        self.output_folder_txt = f"{output_folder}/new_master_accounts.txt"
    
    def calculate_transaction_cost(self, plan):
        if plan == "student":
            return 0.5
        if plan == "non-student":
            return 0.10
        else:
            raise ValueError(f"Plan {plan} not found")
        return 