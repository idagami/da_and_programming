import sqlite3

conn = sqlite3.connect("cumta_alerts.db")
cursor = conn.cursor()

old_column_name = "alert_date"
new_column_name = "alert_datetime"
table_name = "alerts"

try:
    cursor.execute(
        f"""
    ALTER TABLE {table_name} 
    RENAME COLUMN {old_column_name} TO {new_column_name}
    """
    )
    conn.commit()
    print(f"Column '{old_column_name}' renamed to '{new_column_name}' successfully.")
except sqlite3.OperationalError as e:
    print(f"An error occurred: {e}")

conn.close()
