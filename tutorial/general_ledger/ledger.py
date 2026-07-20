# Packages
from dataclasses import dataclass, field, asdict
from datetime import datetime, date
from helpers import parse_date
from decimal import Decimal
import csv

# Ledger line class
@dataclass
class LedgerLine:
    number: int
    date: date
    account: str
    description: str
    debit: Decimal
    credit: Decimal
    running_balance: Decimal

# Create general ledger
def create_general_ledger(general_journal):
    # General ledger & running balances instances
    general_ledger = {}
    running_balances = {}
    
    # Create keys for general ledger & running balances
    for entry in general_journal:
        for line in entry.lines:
            general_ledger[line.account] = []
            running_balances[line.account] = Decimal('0')
    
    # loop over general journal
    for entry in general_journal:
        for line in entry.lines:
            # Update running balances
            running_balances[line.account] += line.debit
            running_balances[line.account] -= line.credit
            
            # Add ledger line
            general_ledger[line.account].append(
                LedgerLine(
                    number = entry.number,
                    date = entry.date,
                    account = line.account,
                    description = entry.description,
                    debit = line.debit,
                    credit = line.credit,
                    running_balance = running_balances[line.account]
                )
            )
            
    # Return general ledger
    return general_ledger

# Export general ledger to CSV
def general_ledger_to_csv(general_ledger, account):
    with open('./reports/' + account + '.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=asdict(general_ledger[account][0]))
        for entry in general_ledger[account]:
            writer.writerow(asdict(entry))