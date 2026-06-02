import sqlite3

conn = sqlite3.connect("tickets.db")
cursor = conn.cursor()

# Delete all tickets
cursor.execute("DELETE FROM tickets")

# Reset auto-increment ID counter
cursor.execute("DELETE FROM sqlite_sequence WHERE name='tickets'")

conn.commit()
conn.close()

print("Database reset successfully.")