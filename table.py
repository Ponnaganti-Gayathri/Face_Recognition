import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('emp_logs.db')
c = conn.cursor()

# Create the logs table
c.execute('''CREATE TABLE IF NOT EXISTS logs (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             empid TEXT,
             entry_time TEXT,
             exit_time TEXT
             )''')

conn.commit()
conn.close()
