from telethon import TelegramClient
import asyncio
import json
import re
from dotenv import load_dotenv
import os
import sqlite3
from datetime import datetime, timezone
import csv
import unicodedata
import string
from dateutil import parser

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
CHANNEL = "@CumtaAlertsEnglishChannel"
OUTPUT_FILE = "cumta_alerts.ndjson"
DB_FILE = "cumta_alerts.db"

# ----------- TEXT PATTERNS WITH RE ---------- #
DATETIME_PATTERN = re.compile(r"__?(\d{2}/\d{2}/\d{4} \d{2}:\d{2}(?::\d{2})?)__?:?")
ALERT_TYPE_PATTERN = re.compile(r"^(.*?) at")
BULLET_PATTERN = re.compile(r"•\s*\**(.+?)\**\s*-\s*(.+)")
BULLET_PATTERN1 = re.compile(r"•\s*(.+?):\s*(.+)")


# Seting date range here
START_DATE = datetime(2025, 12, 29, 0, 0, 1, tzinfo=timezone.utc)
END_DATE = datetime(2026, 1, 4, 23, 59, 59, tzinfo=timezone.utc)


# ---------------- PARSING FUNCTION -----------------------
def parse_message(message):
    rows = []
    if not message.text:
        return rows

    lines = message.text.split("\n")
    first_line = lines[0] if lines else ""
    alert_type_match = ALERT_TYPE_PATTERN.match(first_line)
    alert_type = alert_type_match.group(1).strip() if alert_type_match else None

    splits = DATETIME_PATTERN.split(message.text)

    if len(splits) == 1:
        alert_datetime = message.date.isoformat()
        block_text = message.text
        splits = ["", alert_datetime, block_text]

    for i in range(1, len(splits), 2):
        alert_datetime = splits[i]
        block_text = splits[i + 1]

        for line in block_text.split("\n"):
            line = line.strip()
            if not line.startswith("•"):
                continue

            match = BULLET_PATTERN.match(line)
            match1 = BULLET_PATTERN1.match(line)

            if match:
                alert_zone = match.group(1).strip()
                localities_str = match.group(2).strip()
            elif match1:
                alert_zone = match1.group(1).strip()
                localities_str = match1.group(2).strip()
            else:
                continue  # skip line if no match

            localities = [l.strip() for l in localities_str.split(",") if l.strip()]

            for locality in localities:
                row = {
                    "alert_datetime": alert_datetime,
                    "alert_type": alert_type,
                    "alert_zone": alert_zone,
                    "locality": locality,
                    "raw_message_id": message.id,
                }
                rows.append(row)

    return rows


# ------- REGION PARSING, DATA from CSV -------- #
def normalize_locality(name: str) -> str:
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


def load_city_regions(csv_path: str) -> dict:
    city_to_region = {}

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            region = row["region"].strip() or None

            for key in ("city", "alias1", "alias2", "alias3", "alias4"):
                city_name = row.get(key)
                if city_name:
                    norm = normalize_locality(city_name)
                    city_to_region[norm] = region

    print(f"Loaded {len(city_to_region)} city / region mappings")
    return city_to_region


def normalize_datetime(dt):
    """
    Normalize a datetime to string format: 'YYYY-MM-DD HH:MM:SS'
    Always in UTC
    Works for datetime or string
    """
    if dt is None:
        return None

    # if already datetime object
    if isinstance(dt, datetime):
        dt_utc = (
            dt.astimezone(timezone.utc)
            if dt.tzinfo
            else dt.replace(tzinfo=timezone.utc)
        )
        return dt_utc.strftime("%Y-%m-%d %H:%M:%S")

    # if string
    try:
        dt_parsed = parser.parse(dt, dayfirst=True)
        if dt_parsed.tzinfo:
            dt_parsed = dt_parsed.astimezone(timezone.utc)
        else:
            dt_parsed = dt_parsed.replace(tzinfo=timezone.utc)
        return dt_parsed.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(f"Failed to parse datetime '{dt}': {e}")
        return None


# ---------------- MAIN FUNCTION -----------------------
async def main():
    CITY_REGION_MAP = load_city_regions("citiesregions.csv")

    async with TelegramClient("cumta_export", API_ID, API_HASH) as client:
        print(f"Connected. Fetching messages from {START_DATE} to {END_DATE}...\n")
        all_rows = []

        async for message in client.iter_messages(
            CHANNEL, reverse=True
        ):  # oldest first

            if message.date < START_DATE:
                continue  # skip messages before start
            if message.date > END_DATE:
                break  # stop after end date

            rows = parse_message(message)
            all_rows.extend(rows)

        print(f"Parsed {len(all_rows)} alert rows from messages.")

        # ------ Save NDJSON ------
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            for row in all_rows:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"Saved NDJSON to {OUTPUT_FILE}")

        # ------ Save SQLite ------
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_datetime TEXT,
                alert_type TEXT,
                alert_zone TEXT,
                locality TEXT,
                region TEXT,
                raw_message_id INTEGER
            )
        """
        )
        for row in all_rows:
            norm_locality = normalize_locality(row["locality"])
            region = CITY_REGION_MAP.get(norm_locality)
            alert_datetime_iso = normalize_datetime(row["alert_datetime"])

            cursor.execute(
                """
                INSERT INTO alerts (alert_datetime, alert_type, alert_zone, locality, region, raw_message_id)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    alert_datetime_iso,
                    row["alert_type"],
                    row["alert_zone"],
                    row["locality"],
                    region,
                    row["raw_message_id"],
                ),
            )

        conn.commit()
        conn.close()
        print(f"Saved data to SQLite database {DB_FILE}")


if __name__ == "__main__":
    asyncio.run(main())
