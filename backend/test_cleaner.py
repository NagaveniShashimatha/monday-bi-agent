# backend/test_cleaner.py

from data_cleaner import run_step_3

# Simulated raw API response (like monday.com)
raw_items = [
    {
        "name": "Naruto Deal",
        "column_values": [
            {"title": "Sector", "text": "energy"},
            {"title": "Deal Value", "text": "1,700,000"},
            {"title": "Expected Close Date", "text": ""},
            {"title": "Deal Stage", "text": "Proposal"}
        ]
    },
    {
        "name": "Sasuke Deal",
        "column_values": [
            {"title": "Sector", "text": "ENERGY"},
            {"title": "Deal Value", "text": "2,500,000"},
            {"title": "Expected Close Date", "text": "2025-03-15"},
            {"title": "Deal Stage", "text": "Negotiation"}
        ]
    }
]

# ▶ Run Step 3
result = run_step_3(raw_items)

print(result)
