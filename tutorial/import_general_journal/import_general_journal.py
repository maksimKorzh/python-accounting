# Packages
import json

# General journal entries database
general_journal = []

# Open general journal CSV
with open('General_journal.csv') as f:
    # Split raw entries
    raw_entries = f.read().split('J/E')[1:]
    
    # Loop over raw entries
    for raw_entry in raw_entries:
        # Single journal entry structure
        journal_entry = {
            'number': '',
            'date': '',
            'journal_lines': [],
            'description': ''
        }
        
        # Split raw_entry into rows
        raw_entry_rows = [col.split(',') for col in raw_entry.split('\n')]
        
        # Filter raw entry rows
        if raw_entry_rows[-1] == ['']: del raw_entry_rows[-1]
        if raw_entry_rows[-1] == ['', '', '', '']: del raw_entry_rows[-1]
        
        # Store journal entry data
        journal_entry['number'] = int(raw_entry_rows[0][0].split('#')[-1])
        journal_entry['date'] = raw_entry_rows[1][0] + ', 2025'
        journal_entry['description'] = raw_entry_rows[-1][1]
        
        # Loop over journal entry lines
        for line in raw_entry_rows[1:-1]:
            journal_entry['journal_lines'].append({
                'account': line[1].strip(),
                'debit': int(line[2]) if line[2] else 0,
                'credit': int(line[3]) if line[3] else 0
            })
        
        # Append journal entry to the general journal
        general_journal.append(journal_entry)

# Write general journal into JSON file
with open('General_journal.json', 'w') as f:
    f.write(json.dumps(general_journal, indent=2))

print('Imported "General_journal.csv" to "General_journal.json"')