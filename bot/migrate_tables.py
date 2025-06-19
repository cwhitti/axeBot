import sqlite3

def migrate_section_table(backup_db_path, nau_db_path):
    try:
        # Connect to the backup database
        backup_conn = sqlite3.connect(backup_db_path)
        backup_cursor = backup_conn.cursor()

        # Connect to the NAU database
        nau_conn = sqlite3.connect(nau_db_path)
        nau_cursor = nau_conn.cursor()

        # Fetch all data from the Section table in the backup database
        backup_cursor.execute("SELECT * FROM Section")
        section_data = backup_cursor.fetchall()

        # Get the column names from the backup database
        backup_cursor.execute("PRAGMA table_info(Section)")
        columns = [col[1] for col in backup_cursor.fetchall()]

        # Create a placeholder string for insertion values
        placeholders = ", ".join(["?"] * len(columns))
        insert_query = f"INSERT INTO Section ({', '.join(columns)}) VALUES ({placeholders})"

        # Delete existing data in the Section table in the NAU database (optional)
        nau_cursor.execute("DELETE FROM Section")

        # Insert data into the Section table in the NAU database
        nau_cursor.executemany(insert_query, section_data)

        # Commit the changes and close connections
        nau_conn.commit()
        print("Data migration completed successfully.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        # Close database connections
        if backup_conn:
            backup_conn.close()
        if nau_conn:
            nau_conn.close()

# Paths to the SQLite databases
backup_db_path = "database/backupNAUCourses.db"
nau_db_path = "database/NAUCourses.db"

# Call the function to migrate data
migrate_section_table(backup_db_path, nau_db_path)