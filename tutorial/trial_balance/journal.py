# Packages
from dataclasses import dataclass, field
from datetime import datetime, date
from helpers import parse_date
from accounts import accounts
from decimal import Decimal
from helpers import to_json
import json
import sys

# Journal line class
@dataclass
class JournalLine:
    account: str
    debit: Decimal
    credit: Decimal

# Journal entry class
@dataclass
class JournalEntry:
    number: int
    date: date
    lines: list[JournalLine] = field(default_factory=list)
    description: str = ''
    
    @property
    def total_debits(self) -> Decimal:
        return sum(line.debit for line in self.lines)
    
    @property
    def total_credits(self) -> Decimal:
        return sum(line.credit for line in self.lines)
    
    def is_balanced(self) -> bool:
        return self.total_debits == self.total_credits

# Create general journal
def create_journal(filename):
    # Create general journal
    general_journal = []

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
        print(f'Imported {filename}')
        return general_journal
    else:
        print('Validation failed.')
        sys.exit(1)

# Validate journal entry
def validate_entry(entry: JournalEntry) -> list[str]:
    # list of errors
    errors = []
    
    # Double entry accounting violation
    if len(entry.lines) < 2:
        errors.append('Journal entry must contain at least two lines.')
    
    # Balance issue
    if not entry.is_balanced():
        errors.append('Journal entry is not balanced.')
    
    # Validate each line
    for i, line in enumerate(entry.lines, start=1):
        # Run checks
        if line.account not in accounts:
            errors.append(f'Line {i}: unnknown account "{line.account}".')
        
        if line.debit < 0:
            errors.append(f'Line {i}: negative debit.')
        
        if line.credit < 0:
            errors.append(f'Line {i}: negative credit.')
        
        if line.debit > 0 and line.credit > 0:
            errors.append(f"Line {i}: both debit and credit specified.")

        if line.debit == 0 and line.credit == 0:
            errors.append(f"Line {i}: neither debit nor credit specified.")
    
    # Return list of errors
    return errors

# Validate general journal
def validate_general_journal(general_journal):
    # Whether journal has errors
    no_errors = True
    
    # Loop over journal entries
    for entry in general_journal:
        errors = validate_entry(entry)
    
        # Print errors if any
        if errors:
            no_errors = False
            print(f'Journal Entry #{entry.number} is invalid:')
            for error in errors:
                print(f'  - {error}')
        
        # Print success otherwise
        else:
            print(f'Journal Entry #{entry.number} is valid')
    
    # Return validation status
    return no_errors

# Write general journal into JSON file
def general_journal_to_json(general_journal):
    with open('./reports/General_journal.json', 'w') as f:
        f.write(json.dumps([to_json(entry) for entry in general_journal], indent=2))