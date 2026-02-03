import csv
import sqlite3
from pathlib import Path
import unicodedata
import string
import re

DB_PATH = "cumta_alerts.db"
TABLE_NAME = "alerts"
LOCALITY_COL = "locality"
REGION_COL = "region"

CSV_PATH = "citiesregions.csv"
DRY_RUN = False
# DRY_RUN = True  # True = no DB updates, just preview statistics


def normalize_city(name: str) -> str:
    if not name:
        return ""

    name = unicodedata.normalize("NFKD", name)
    name = "".join(c for c in name if not unicodedata.category(c).startswith("M"))
    name = re.sub(r"[\u200e\u200f\u202a-\u202e]", "", name)
    name = name.replace("\u00a0", " ")
    name = re.sub(r"\(.*?\)", "", name)
    name = name.split(" - ")[0]
    name = (
        name.lower()
        .replace("`", "'")
        .replace("’", "'")
        .replace('"', "")
        .replace("''", "")
        .replace("-", " ")
    )
    name = name.translate(str.maketrans("", "", string.punctuation))
    name = re.sub(r"\s+", " ", name).strip()

    return name


def load_city_region_map(csv_path):
    """
    Returns:
      dict[str, str]  -> locality_name -> region
    """
    mapping = {}

    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        # utf8sig - strings the csv column indexes of invisible signs that it had
        reader = csv.DictReader(f)
        print("CSV headers detected:", reader.fieldnames)

        for row in reader:
            region = row.get("region", "").strip()
            if not region:
                continue

            for key in ["city", "alias1", "alias2", "alias3", "alias4"]:
                name = row.get(key, "")
                if name:
                    mapping[normalize_city(name)] = region

    return mapping


def main():
    if not Path(DB_PATH).exists():
        raise FileNotFoundError(DB_PATH)

    city_region = load_city_region_map(CSV_PATH)
    print(f"Loaded {len(city_region)} cities / region mappings")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        f"""
        SELECT rowid, {LOCALITY_COL}, {REGION_COL}
        FROM {TABLE_NAME}
    """
    )
    rows = cur.fetchall()

    updated = 0
    skipped = 0
    unmatched = 0

    for rowid, locality, current_region in rows:
        if not locality:
            skipped += 1
            continue

        key = normalize_city(locality)

        if key not in city_region:
            unmatched += 1
            continue

        new_region = city_region[key]

        if (current_region or "").strip() == new_region.strip():
            skipped += 1
            continue

        if not DRY_RUN:
            cur.execute(
                f"""
                UPDATE {TABLE_NAME}
                SET {REGION_COL} = ?
                WHERE rowid = ?
                """,
                (new_region, rowid),
            )

        updated += 1

    if not DRY_RUN:
        conn.commit()

    conn.close()

    print("----- RESULT -----")
    print(f"Updated rows   : {updated}")
    print(f"Skipped rows   : {skipped}")
    print(f"Unmatched rows : {unmatched}")
    print(f"Dry run        : {DRY_RUN}")


if __name__ == "__main__":
    main()
