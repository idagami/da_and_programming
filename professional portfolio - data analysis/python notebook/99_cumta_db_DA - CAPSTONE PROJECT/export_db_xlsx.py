import sqlite3
from openpyxl import Workbook

DB_PATH = "cumta_alerts.db"
OUTPUT_XLSX = "exported_data.xlsx"

TABLE = "alerts"
REGION_COL = "region"


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # cur.execute(f"SELECT * FROM {TABLE}")

    # only distinct localities from whole table
    cur.execute(f"SELECT DISTINCT locality, city FROM {TABLE}")

    # # only rows where region is null
    # cur.execute(
    #     f"""
    #     SELECT *
    #     FROM {TABLE}
    #     WHERE {REGION_COL} IS NULL
    #        OR TRIM({REGION_COL}) = ''
    # """
    # )

    # # Only rows with region filled
    # cur.execute(
    #     f"""
    #     SELECT *
    #     FROM {TABLE}
    #     WHERE {REGION_COL} IS NOT NULL
    #        AND TRIM({REGION_COL}) != ''
    # """
    # )

    # # Order by time
    # cur.execute(
    #     f"""
    #     SELECT * FROM alerts ORDER BY alert_datetime
    # """
    # )

    # # Export by datetime range
    # START = "2025-10-01T00:00:00"
    # END   = "2025-10-31T23:59:59"
    # cur.execute(
    #     f"""
    #     SELECT *
    #     FROM alerts
    #     WHERE alert_datetime BETWEEN ? AND ?
    #     ORDER BY alert_datetime
    #     """,
    #     (START, END)
    # )

    # # single region
    # REGION = "Tel Aviv"
    # cur.execute(
    #     f"""
    #     SELECT *
    #     FROM alerts
    #     WHERE region = ?
    #     ORDER BY alert_datetime
    #     """,
    #     (REGION,)
    # )

    # # multiple regions
    # cur.execute(
    #     """
    # SELECT *
    # FROM alerts
    # WHERE region IN ('North', 'Center', 'South')
    # ORDER BY alert_datetime
    # """
    # )

    # # partial match
    # cur.execute(
    #     """
    # SELECT *
    # FROM alerts
    # WHERE region IN ('North', 'Center', 'South')
    # ORDER BY alert_datetime
    # """
    # )

    # # combining filters
    # cur.execute(
    #     """
    # SELECT *
    # FROM alerts
    # WHERE region = 'South'
    #   AND alert_datetime BETWEEN '2025-10-01' AND '2025-10-31'
    # ORDER BY alert_datetime
    # """
    # )

    # # aggregation
    # cur.execute(
    #     """
    # SELECT region, COUNT(*)
    # FROM alerts
    # GROUP BY region
    # ORDER BY COUNT(*) DESC
    # """
    # )

    rows = cur.fetchall()
    headers = [d[0] for d in cur.description]

    conn.close()

    print(f"Found {len(rows)} rows")

    wb = Workbook()
    ws = wb.active
    ws.title = "Missing Region"

    ws.append(headers)

    for row in rows:
        ws.append(row)

    wb.save(OUTPUT_XLSX)
    print(f"Saved to {OUTPUT_XLSX}")


if __name__ == "__main__":
    main()
