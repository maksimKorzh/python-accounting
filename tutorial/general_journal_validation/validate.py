# Packages
from journal import JournalEntry

# Validate journal entry
def validate_entry(entry: JournalEntry) -> list[str]:
    # list of errors
    errors = []
    
    # List of accounts
    accounts = [
        'Cash',
        'Supplies',
        'Equipment',
        'Accounts payable',
        'Loans payable',
        'Owner\'s capital',
        'Revenue',
        'Cost os services',
        'Laundry costs'
    ]
    
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