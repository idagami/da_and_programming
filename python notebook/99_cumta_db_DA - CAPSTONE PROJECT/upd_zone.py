# upd_zone.py
import csv
import sqlite3
from pathlib import Path
import re

DB_PATH = "cumta_alerts.db"  # path to your DB
TABLE_NAME = "alerts"  # table name
ALERT_ZONE_COL = "alert_zone"  # column to update
DRY_RUN = False
# DRY_RUN = True  # set True to only preview changes without DB update

# Mapping for renaming / merging zones
names_adj_map = {
    "אשדוד": "Ashdod",
    "נילי": "Nili",
    "נירים": "Nirim",
    "NIrim": "Nirim",
    "פרדס חנה": "Pardes Hana",
    "צפת": "Zefat",
    "לב החולה": "Lev HaChula",
    "שדרות  איבים  ניר עם": "Sderot / Nir Am",
    "רפטינג נהר הירדן": "Jordan Rafting",
    "Confrontation line": "Confrontation Line",
    "Gaza containment": "Gaza Containment",
    "Southern Negev": "South Negev",
    "Western Negev": "West Negev",
    "Central Negev": "Center Negev",
    "Menashe Aviel Or Akiva Caesarea Industrial Alonei Itzhak Beit Hanania Binyamina Jisr az": "Menashe",
    "Menashe Hadera": "Menashe",
    "Shfela (Lowlands)": "HaShfela",
    "HaShfela Palmachim Rishon LeZion": "HaShfela",
    "HaShfela Rishon LeZion": "HaShfela",
    "Lachish": "Lakhish",
    "Wadi Ara bqa al": "Wadi Ara",
    "Western Lakhish": "West Lakhish",
    "Lakhish Ashdod": "Ashdod",
    "Lakhish Beit Ezra Givati Ezer Azrikam Sdeh Uziahu Re'em Industrial Park Ad Halom Industrial Ashdod": "Lakhish",
    "Lakhish Bitzaron Gan Yavne Kannot Ashdod": "Lakhish",
    "Lakhish Emunim Beit Ezra Givati Ezer Azrikam Sdeh Uziahu Shtulim Re'em Industrial Park Ad Halom Industrial Ashdod": "Lakhish",
    "Lakhish Hatzav Hatzor Emunim Beit Ezra Givati Ezer Azrikam Sdeh Uziahu Shtulim Re'em Industrial Park Ad Halom Industrial Ashdod": "Lakhish",
    "Lakhish Merkaz Shapira Masuot Itzhak Ein Tzurim Shafir Ashdod": "Lakhish",
    "Lakhish Ad Halom Industrial Ashdod": "Lakhish",
}


def clean_alert_zone(value: str) -> str:
    """
    Clean and normalize a single alert_zone string
    """
    if not value:
        return ""

    value = str(value)
    value = re.sub(r"[\"“”]", "", value)  # remove quotes
    value = re.sub(r"\*+", "", value)  # remove stars
    value = re.sub(r"\bArea\b|\bZone\b", "", value, flags=re.IGNORECASE)
    value = re.sub(r":", "", value)  # remove colons
    value = re.sub(r"\\,", " ", value)  # replace escaped commas with space
    value = re.sub(r",", " ", value)  # replace commas with space
    value = re.sub(r"\d+$", "", value)
    value = re.sub(r"\s+", " ", value)  # normalize spaces
    value = value.strip()
    return value


def apply_mapping(value: str, mapping: dict) -> str:
    """
    Replace a string using the mapping dictionary
    """
    for old, new in mapping.items():
        pattern = re.escape(old)
        value = re.sub(pattern, new, value)
    return value.strip()


def main():
    if not Path(DB_PATH).exists():
        raise FileNotFoundError(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(f"SELECT rowid, {ALERT_ZONE_COL} FROM {TABLE_NAME}")
    rows = cur.fetchall()

    updated = 0
    skipped = 0

    for rowid, alert_zone in rows:
        if not alert_zone:
            skipped += 1
            continue

        # 1️⃣ Apply mapping first
        mapped = apply_mapping(alert_zone, names_adj_map)

        # 2️⃣ Clean the string
        cleaned = clean_alert_zone(mapped)

        if cleaned == (alert_zone or "").strip():
            skipped += 1
            continue

        if not DRY_RUN:
            cur.execute(
                f"UPDATE {TABLE_NAME} SET {ALERT_ZONE_COL} = ? WHERE rowid = ?",
                (cleaned, rowid),
            )

        updated += 1

    if not DRY_RUN:
        conn.commit()
    conn.close()

    print("----- RESULT -----")
    print(f"Updated rows: {updated}")
    print(f"Skipped rows: {skipped}")
    print(f"Dry run     : {DRY_RUN}")


if __name__ == "__main__":
    main()
