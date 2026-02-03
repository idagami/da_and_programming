# Israel Alert Data Analysis Project

## Project Overview

This project performs a detailed analysis of security alerts sounded across Israel.  
The goal is to identify spatial and temporal patterns, including:

- Whether specific localities or regions are affected more frequently
- Time-of-day trends in alerts
- Regional concentration of different alert types
- Other recurring or hidden patterns in alert activity

Each alert is analyzed at the **locality level**, allowing for high-resolution geographic insights.

---

## Data Description

- Each row in the database represents **one alert in one specific locality**
- A single security incident (rocket, drone, terrorism, etc.) may affect multiple localities — each is recorded separately
- Every row has a **unique ID**
- As of **December 28, 2025**, the database contains:
  - **100,324 alert entries**
  - **20 entries with missing region values**

### Geographic Hierarchy

```
Region (one)
 └── City (many)
      └── Locality / Neighborhood (many)
```

---

## Important File Notice

**DO NOT delete** the file:

```
cumta_export.session
```

If deleted, Telegram credentials will need to be re-entered.

---

## Project Engine

- **Main script:** `my_main.py`
- The script **overwrites** the existing `.ndjson` export file (does not append)
- To change behavior to append mode, modify:

```python
with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
```

- Despite overwriting exports, **database entries remain precise and persistent**

---

## Execution Order

Scripts should be executed in the following order:

1. **`check_oldest_msg.py`**  
   Finds the oldest message to enable gradual export in batches.

2. **`upd_alerttype.py`**  
   Updates missing alert types using manual Excel annotation.

3. **`upd_ashdod_locality.py`**  
   Normalizes Ashdod localities and aliases.

4. **`upd_region.py`**  
   Populates region values based on external CSV mappings.

5. **`upd_zone.py`**  
   Merges duplicated alert zones using a manually created dictionary.

6. **`upd_city.py`**  
   Creates and populates a `city` column to avoid fragmented city entries.

---

## Helper Scripts

- **`export_db_xlsx.py`** – Export database content to Excel (full or filtered)
- **`renaming_column.py`** – Column renaming utility

---

## Alert Type Completion Logic

Some alerts are split across multiple messages, with the alert type only appearing in the first one.

**Process:**

1. If `type_update.xlsx` exists → missing types are updated
2. Otherwise → an Excel file is generated with missing entries + preceding messages
3. Alert types are manually filled and the script is re-run

---

## Regional & City Normalization Notes

### Ashdod Case

- Over 30 aliases and districts normalized
- Alert count increased from **19 → 2,099**
- Change is irreversible → database backups are essential

### City Column

- New `city` column prevents destructive normalization
- Neighborhood-level detail is preserved for deeper analysis

---

## Region Mapping Logic

- Regions are populated from an **external manually maintained CSV**
- Mapping is done per locality, not per alert zone
- Aliases are continuously added as new alerts arrive

To update:

- Fetch new alerts → `my_main.py`
- Populate missing regions → `upd_region.py`

---

## Special Regional Handling

- **Tel Aviv Region:** Herzliya → Bat Yam (~10 km radius)
- **Center Region:** Netanya, Rishon, Ashdod

Tel Aviv is a major employment hub, so daytime alerts may affect commuters from outside the region.

---

## Presentation Output

Notebook outputs can be converted to slides:

- Run: `ntb_to_ppt.py`
- Supports text, tables, and matplotlib charts
- Plotly charts are not supported

---

## Notes

- Alerts continue to occur daily
- Database and mappings are regularly updated
- Project is designed for iterative re-execution
