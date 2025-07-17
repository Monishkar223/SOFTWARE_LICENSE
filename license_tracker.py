

import sqlite3
from datetime import datetime, timedelta

# Connect to SQLite DB
conn = sqlite3.connect('license_tracker.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS licenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        software TEXT NOT NULL,
        license_key TEXT NOT NULL,
        expiry_date DATE NOT NULL
    )
''')
conn.commit()

def add_license():
    software = input("Enter software name: ")
    license_key = input("Enter license key: ")
    expiry = input("Enter expiry date (YYYY-MM-DD): ")
    cursor.execute("INSERT INTO licenses (software, license_key, expiry_date) VALUES (?, ?, ?)",
                   (software, license_key, expiry))
    conn.commit()
    print("License added successfully!")

def search_license():
    name = input("Enter software name to search: ")
    cursor.execute("SELECT * FROM licenses WHERE software LIKE ?", ('%' + name + '%',))
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def view_all():
    cursor.execute("SELECT * FROM licenses")
    for row in cursor.fetchall():
        print(row)

def view_upcoming_expiries():
    today = datetime.today().date()
    upcoming = today + timedelta(days=30)
    cursor.execute("SELECT * FROM licenses WHERE expiry_date BETWEEN ? AND ?", (today, upcoming))
    rows = cursor.fetchall()
    print(f"Licenses expiring within 30 days ({today} to {upcoming}):")
    for row in rows:
        print(row)

# CLI Menu
while True:
    print("\n--- License Tracker Menu ---")
    print("1. Add License")
    print("2. Search License")
    print("3. View All Licenses")
    print("4. View Upcoming Expiries")
    print("5. Exit")

    choice = input("Enter choice: ")
    if choice == '1':
        add_license()
    elif choice == '2':
        search_license()
    elif choice == '3':
        view_all()
    elif choice == '4':
        view_upcoming_expiries()
    elif choice == '5':
        break
    else:
        print("Invalid choice.Try again.")
