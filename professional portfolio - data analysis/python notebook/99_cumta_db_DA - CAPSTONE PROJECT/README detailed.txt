My project created to perform detailed analysis on the various type of alerts sounded in Israel, 
to see if there is any tendency for specific localities or regions, if certain areas are hit more often 
or alerts sound on specific time of the day or to find any other possible pattern in alerts.

DO NOT delete file cumta_export.session. Otherwise will need to provide Telegram credentials once again.


The engine of the project is my_main.py
It does not append to .ndjson file, but overwrites the old info with new exported data.
to change: 'with open(OUTPUT_FILE, "a", encoding="utf-8") as f:'
However the data saved into db is very precise.

Order of execution:
- check_oldest_msg.py (to find the starting date so can star the gradual export in bulks)
- upd_alerttype.py (Manually in Excel I added correct type and db then got updated with values saved in Excel: raw_msg_id : alert type)
- upd_ashdod_locality.py (explained above)
- upd_region.py (based on csv column)
- upd_zone.py (manual assessment was done to the originally export list and many duplicates were found (i.e. Northern Lakshish and Lakshish North). 
A dictionary was put together to enable the merger.)
- upd_city.py ('city' column isnt originally in the db, we populate it based on info in our csv. 
Value of city is either locality or if at least one alias exists - first locality in the row; 
to avoid city entries like "Tel Aviv NOrth, Tel Aviv West. Now all fall under Tel Aviv)

Helper files:
- export_db_xlsx.py (to export the data fully or filtered into Excel. There are few commented code snippets inside: 
the extract all data or the data with the regions missing or extract certain rows under conditions / filters.)
- renaming_column.py

In order to be able to present the results to the team, the notebook outputs can be turned into slides of a presentation.
FOr this run code ntb_to_ppt.py. However, it only exports the text / tables and matplotlib charts and not plotly.


Notes:
By Dec 28 2025 the db included 100324 alert entries, among which 20 had null region.

Each row in the table represents an alert in specific locality. Per each security incident (rocket, drone, 
terrorism etc) few localities may have been affected. ALl those localities have seen taken one-by-one
to facilitate detailed analysis. Each row has a unique id.

Geo hierarchy: region(one) - city(many) - locality(many many).

The column 'region' is not populated from the alerts data, however from the external csv 
that i put together manually from many sources (as per locality, not by the alert_zone). 
The csv includes the locality and it's multiple aliases found within the alerts or online.
I continuosly add aliases and sadly more alerts are coming daily, 
so i will be rerunning the code and updating the db. If needed to check for more alerts, run my_main.py.
If localities file was updated and we want to update region names for entries which are missing them in db, run upd_region.py

The column 'alert_type' had many missing value. it's due that some alerts are that long 
so they are split into few messages, and the alert type isn't mentioned at the beginning of each, only
at the beginning of the first one. So can use file upd_alerttype.py and it will first check 
if type_update.xlsx exists, then it will update missing type entries in db. 
If not, it will export the xlsx with ids and msgs that are missing the alert_type 
and 2 msgs preceding them as teh type is most likely written in those. I extracted alert_type from 
those previous msgs and saved into type_update.xlsx file and re-run the .py file. 
the db then got updated.

Ashdod had over 30 aliases and smaller districts which belong to it. So i normalized them ('upd_ashdod.py)
to have a clear picture of Ashdod alerts. Suddenly Ashdod numbers spiked from 19 to 2099, 
which put it on top of the list (comparing to 594 in Kiryat Shmona). I saved this action into the db 
and cannot undo it. Therefore I learnt that having db backup before any operations is essential.
To avoid further mistakes, I created a new column 'city' where i normalized the known districts into city.
THe purpose of analysis is to see where citizens are more disturbed and an alert in one district of the city
will definitely disturb citizens of nearby district. 
Locality / neighborhoods column can be then used for further detalization.

Tel Aviv and surroundings within 10 km+- were moved into a separate region - 'Tel Aviv', 
while areas around this region are still considered 'Center. Areas from Herzliya till Bat Yam incl are 'Tel Aviv' region.
Netania, Rishon, Ashdod - 'Center'. Also important to remember that 'Tel Aviv' is the region where many people go for work
during the day, therefore alerts during the daytime affect those living away from this region.