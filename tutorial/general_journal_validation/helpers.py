# Packages
from dataclasses import asdict
from datetime import datetime, date
import re

# Parse date helper
def parse_date(date_str: str) -> date:
    cleaned_date = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)
    return datetime.strptime(cleaned_date, '%b %d, %Y').date()

# Convert journal entry to JSON
def to_json(entry):
    # Convert entry to dict
    d = asdict(entry)
    d['date'] = entry.date.isoformat()
    
    # Make values JSON friendly
    for line in d['lines']:
        line['debit'] = str(line['debit'])
        line['credit'] = str(line['credit'])
    
    # Return dict
    return d