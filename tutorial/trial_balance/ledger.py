# Packages
from dataclasses import dataclass, field, asdict
from datetime import datetime, date
from helpers import parse_date
from accounts import accounts
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
    for account in accounts:
        general_ledger[account] = []
        running_balances[account] = Decimal('0')
    
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

# Report trial balance
def trial_balance(general_ledger, month, year):
    # Trial balance table
    balance_list = []
    
    # Loop over general ledger accounts
    for account in general_ledger.keys():
        for line in general_ledger[account]:
            if line.date.month == month and line.date.year == year:
                balance_line = {
                    'account': account,
                    'debit': line.running_balance if line.running_balance > 0 else '',
                    'credit': (line.running_balance * -1) if line.running_balance < 0 else '',
                }

        # Append balance line to trial balance
        balance_list.append(balance_line)

    # Total debits & credits
    total_debits = 0
    total_credits = 0

    # Calculate total debits & credits
    for line in balance_list:
        if line['debit']: total_debits += line['debit']
        if line['credit']: total_credits += line['credit']

    # Check balance
    if total_debits != total_credits:
        print(f'Trial balance (Debit: {total_debits}; Credit: {total_credits}) is not balanced')
        return {}, (total_debits == total_credits), total_debits
    else:
       return balance_list, (total_debits == total_credits), total_debits

# Export trial balance to CSV
def trial_balance_to_csv(trial_balance, total, date):
    with open('./reports/trial_balance-' + date + '.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=trial_balance[0])
        for line in trial_balance:
            writer.writerow(line)
        f.write(f'TOTAL,{total},{total}')

# Export general ledger to CSV
def general_ledger_to_csv(general_ledger, account):
    with open('./reports/' + account + '.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=asdict(general_ledger[account][0]))
        for entry in general_ledger[account]:
            writer.writerow(asdict(entry))