import sqlite3
import unicodedata
import re
import string

DB_PATH = "cumta_alerts.db"
TABLE_NAME = "alerts"
LOCALITY_COL = "locality"
# DRY_RUN = True  # CHANGED TO False to make real changes
DRY_RUN = False


# -------- normalization --------
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


# -------- YOUR ASHDOD LIST --------
ASHDOD_ALIASES_RAW = [
    "Ashdod",
    "Ashdod - Northern Industrial Zone and port",
    "Ashdod - Alef",
    "Ashdod - Gimmel",
    "Ashdod - Het",
    "Ashdod-11",
    "Ashdod - Yod Alef",
    "Alef",
    "Bet",
    "Gimmel",
    "Dalet",
    "Heh",
    "Vav",
    "Zain",
    "Het",
    "Tet",
    "Yod",
    "Yod Alef",
    "Yod Bet",
    "Yod Gimmel",
    "Yod Dalet",
    "Yod Zain",
    "Marine",
    "Marina",
    "City",
    "Port",
    "Northern Industrial Zone",
    "Ad Halom Industrial Zone",
    "אשדוד",
    "יא",
    "יב",
    "טו",
    "יז",
    "מרינה",
]

ASHDOD_ALIASES = {normalize_city(x) for x in ASHDOD_ALIASES_RAW}


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(f"SELECT rowid, {LOCALITY_COL} FROM {TABLE_NAME}")
    rows = cur.fetchall()

    updated = 0
    skipped = 0

    for rowid, locality in rows:
        if not locality:
            skipped += 1
            continue

        norm = normalize_city(locality)

        if norm not in ASHDOD_ALIASES:
            skipped += 1
            continue

        if locality == "Ashdod":
            skipped += 1
            continue

        if not DRY_RUN:
            cur.execute(
                f"""
                UPDATE {TABLE_NAME}
                SET {LOCALITY_COL} = ?
                WHERE rowid = ?
                """,
                ("Ashdod", rowid),
            )

        updated += 1

    if not DRY_RUN:
        conn.commit()

    conn.close()

    print("----- RESULT -----")
    print(f"Updated rows : {updated}")
    print(f"Skipped rows : {skipped}")
    print(f"Dry run     : {DRY_RUN}")


if __name__ == "__main__":
    main()
