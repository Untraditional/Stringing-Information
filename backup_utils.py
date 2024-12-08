import os
import shutil

def backup_database_on_launch():
    database_file = "stringing.db"
    backup_dir = "backup"
    backup_file = os.path.join(backup_dir, "stringing_backup.db")  # Fixed backup file name

    # Ensure the backup directory exists
    os.makedirs(backup_dir, exist_ok=True)

    # Delete the old backup if it exists
    if os.path.exists(backup_file):
        try:
            os.remove(backup_file)
            print("Old backup deleted.")
        except Exception as e:
            print(f"Failed to delete old backup: {e}")

    # Create a new backup
    try:
        shutil.copy(database_file, backup_file)
        print(f"Backup created: {backup_file}")
    except Exception as e:
        print(f"Failed to create backup: {e}")
