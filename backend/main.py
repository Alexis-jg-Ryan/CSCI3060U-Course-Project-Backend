from BackendSystem import BackendSystem

MASTER_ACCOUNTS_PATH     = "input/old_master_accounts.txt"
MERGED_TRANSACTIONS_PATH = "input/merged_transactions.txt"
OUTPUT_CURRENT_PATH      = "output/current_accounts.txt"
OUTPUT_MASTER_PATH       = "output/new_master_accounts.txt"

'''
# MAIN entry point for the backend system 
# This function takes in the database files (input/output)
# and then runs the backend system and applies the required
# transactions 
'''
def main():
    backend = BackendSystem(
        master_accounts_path=MASTER_ACCOUNTS_PATH,
        merged_transactions_path=MERGED_TRANSACTIONS_PATH,
        output_current_path=OUTPUT_CURRENT_PATH,
        output_master_path=OUTPUT_MASTER_PATH,
    )
    backend.run()
    print("Backend processing complete.")

if __name__ == '__main__':
    main()