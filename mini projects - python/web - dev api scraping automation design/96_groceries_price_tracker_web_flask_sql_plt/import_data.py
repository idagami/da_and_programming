# this was already done, data inserted into real db, do not re-run!!!

import pandas as pd
import sqlite3
from datetime import datetime
import os

cur_dir = os.path.dirname(__file__)
csv_path = os.path.join(cur_dir, "static", "import_data", "Book1.csv")

db_path = "instance/groceries_db.db"

df = pd.read_csv(csv_path)

df["date"] = pd.to_datetime(df["date"]).dt.date

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

for _, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO groceries (date, shop, item, descr, category, weight, units, cost, price_kg, price_unit)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            row.get("date"),
            row.get("shop"),
            row.get("item"),
            row.get("descr"),
            row.get("category"),
            row.get("weight"),
            row.get("units"),
            row.get("cost"),
            row.get("price_kg"),
            row.get("price_unit"),
        ),
    )

conn.commit()
conn.close()
print("Database populated from CSV!")
