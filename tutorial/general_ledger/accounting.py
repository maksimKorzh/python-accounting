# Packages
from journal import JournalEntry
from journal import JournalLine
from journal import create_journal
from journal import general_journal_to_json
from ledger import create_general_ledger
from ledger import general_ledger_to_csv

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