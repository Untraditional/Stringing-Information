import os
import shutil
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

def backup_database_on_launch():
    database_file = "stringing.db"
    backup_dir = "backup"
    backup_file = os.path.join(backup_dir, "stringing_backup.db")
    excel_backup_file = os.path.join(backup_dir, "stringing_backup.xlsx")
    last_backup_file = os.path.join(backup_dir, "last_backup.txt")  # File to track last backup date

    # Ensure the backup directory exists
    os.makedirs(backup_dir, exist_ok=True)

    # Check the last backup date
    last_backup_date = None
    if os.path.exists(last_backup_file):
        try:
            with open(last_backup_file, "r") as file:
                last_backup_date = datetime.strptime(file.read().strip(), "%Y-%m-%d")
        except Exception as e:
            print(f"Failed to read last backup date: {e}")

    # Determine if a backup is needed
    if last_backup_date and (datetime.now() - last_backup_date).days < 30:
        print("Backup not needed. Last backup was less than a month ago.")
        return

    # Delete the old backups if they exist
    for file in [backup_file, excel_backup_file]:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"Old backup deleted: {file}")
            except Exception as e:
                print(f"Failed to delete old backup: {e}")

    # Create a new .db backup
    try:
        shutil.copy(database_file, backup_file)
        print(f"Database backup created: {backup_file}")
    except Exception as e:
        print(f"Failed to create database backup: {e}")

    # Create a new Excel backup
    try:
        conn = sqlite3.connect(database_file)
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = [row[0] for row in conn.execute(query).fetchall()]

        with pd.ExcelWriter(excel_backup_file, engine='openpyxl') as writer:
            for table in tables:
                df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
                df.to_excel(writer, sheet_name=table, index=False)

        conn.close()
        print(f"Excel backup created: {excel_backup_file}")
    except Exception as e:
        print(f"Failed to create Excel backup: {e}")

    # Update the last backup date
    try:
        with open(last_backup_file, "w") as file:
            file.write(datetime.now().strftime("%Y-%m-%d"))
        print(f"Last backup date updated: {datetime.now().strftime('%Y-%m-%d')}")
    except Exception as e:
        print(f"Failed to update last backup date: {e}")
