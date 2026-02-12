import csv
import sqlite3


DB_PATH = "cumta_alerts.db"
TABLE = "alerts"
CSV_PATH = "citiesregions.csv"

# Build reverse lookup from CSV (for faster lookup) ---
alias_to_city = {}  # alias or canonical -> canonical city

with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header
    for row in reader:
        city = row[0].strip()
        aliases = [alias.strip() for alias in row[1:5] if alias.strip()]
        # Canonical city maps to itself
        alias_to_city[city] = city
        # Aliases map to canonical city
        for alias in aliases:
            alias_to_city[alias] = city

conn = sqlite3.connect(DB_PATH)  # change to your DB
cursor = conn.cursor()

# 'city' column exists ---
try:
    cursor.execute(f"ALTER TABLE {TABLE} ADD COLUMN city TEXT")
    print(f"Added 'city' column to {TABLE} table.")
except sqlite3.OperationalError as e:
    if "duplicate column" in str(e).lower():
        print("'city' column already exists.")
    else:
        raise

cursor.execute(f"SELECT id, city FROM {TABLE}")
rows = cursor.fetchall()

# --- Step 4: Update city column based on CSV ---
for row_id, city_value in rows:
    city_clean = (city_value or "").strip()
    # Normalize: find canonical city or keep as-is if not found
    city_normalized = alias_to_city.get(city_clean, city_clean)
    cursor.execute(
        f"UPDATE {TABLE} SET city = ? WHERE id = ?", (city_normalized, row_id)
    )

conn.commit()
conn.close()

print("City column normalized successfully!")
