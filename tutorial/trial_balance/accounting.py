# Packages
from journal import general_journal_to_json
from journal import create_journal
from journal import JournalEntry
from journal import JournalLine
from ledger import create_general_ledger
from ledger import general_ledger_to_csv
from ledger import trial_balance_to_csv
from ledger import trial_balance

# General journal entries database
general_journal = []

# Create general journal
general_journal = create_journal('General_journal.csv')

# Create general ledger
general_ledger = create_general_ledger(general_journal)

# Export general journal to JSON
general_journal_to_json(general_journal)

# Export general ledger to CSV
for account in general_ledger.keys():
    general_ledger_to_csv(general_ledger, account)

# Calculate trial balance
trial_balance, balance, total = trial_balance(general_ledger, 9, 2025)

# Export trial balance to CSV
if balance:
    trial_balance_to_csv(trial_balance, total, '09-2025')