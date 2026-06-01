import sqlite3

# Connect to database
conn = sqlite3.connect("tickets.db")

# Create cursor
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_text TEXT,
    category TEXT,
    priority TEXT
)
""")

# Save changes
conn.commit()

# Close connection
conn.close()

print("Database created successfully!")