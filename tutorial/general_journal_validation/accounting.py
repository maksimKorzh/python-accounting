# Packages
from journal import JournalEntry, JournalLine
from validate import validate_general_journal
from helpers import parse_date, to_json
from decimal import Decimal
import json

# General journal entries database
general_journal = []

# Create general journal
def create_journal(filename):
    # Open general journal CSV
    with open(filename) as f:
        # Split raw entries
        raw_entries = f.read().split('J/E')[1:]
        
        # Loop over raw entries
        for raw_entry in raw_entries:
            # Split raw_entry into rows
            raw_entry_rows = [col.split(',') for col in raw_entry.split('\n')]
            
            # Filter raw entry rows
            if raw_entry_rows[-1] == ['']: del raw_entry_rows[-1]
            if raw_entry_rows[-1] == ['', '', '', '']: del raw_entry_rows[-1]
            
            # Create journal entry
            journal_entry = JournalEntry(
                number = int(raw_entry_rows[0][0].split('#')[-1]),
                date = parse_date(raw_entry_rows[1][0] + ', 2025'),
                description = raw_entry_rows[-1][1]
            )
            
            # Loop over journal entry lines
            for line in raw_entry_rows[1:-1]:
                journal_line = JournalLine(
                    account = line[1].strip(),
                    debit = Decimal(line[2] if line[2] else '0'),
                    credit = Decimal(line[3] if line[3] else '0')
                )
                journal_entry.lines.append(journal_line)
            
            # Append journal entry to the general journal
            general_journal.append(journal_entry)

    # Validate general journal
    if validate_general_journal(general_journal):
        # Write general journal into JSON file
        with open('General_journal.json', 'w') as f:
            f.write(json.dumps([to_json(entry) for entry in general_journal], indent=2))

        print(f'Imported {filename}')
    
    else:
        print('Validation failed.')

# Create general journal
create_journal('General_journal.csv')