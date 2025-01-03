import sqlite3

# Create a connection to the database
conn = sqlite3.connect('my_database.db')

# Create a cursor object
cursor = conn.cursor()

# Create a table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_basal_rate (
        id_user INTEGER, 
        basal_rate REAL
    );
''')

# Insert data
cursor.execute("INSERT INTO users (name) VALUES (?)", ('Alice', ))
cursor.execute("INSERT INTO users (name) VALUES (?)", ('Bob', ))

# Commit changes
conn.commit()

# Fetch data
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()