# Packages
from dataclasses import dataclass, field, asdict
from datetime import datetime, date
from decimal import Decimal

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