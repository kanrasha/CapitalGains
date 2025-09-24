"""0.3 UPDATE NOTES:
- creates just one MAIN_CSV
- ensures there is a proceeds column
- ensures buy transactions get a cost basis value, sell transactions get a proceeds value
- added tolerance for empty "Fee" column

TO DO
- fix safedate()
- AddEXPORT_DIR.mkdir(exist_ok=True) to your code so your program is resilient and never fails due to a missing directory, no matter how the user obtained or modified the files.

reminder: the function of file_prep is to make any file compatible by formatting it to the program's liking"""


import csv, shutil, re
from datetime import datetime
from pathlib import Path
from decimal import Decimal
import yaml

with open('paths.yaml', 'r') as f:
    config = yaml.safe_load(f)

ROOT            = Path(__file__).parent
WORKING_DIR     = ROOT/config['WORKING_DIR']
IMPORT_CSV      = ROOT/config['IMPORT_CSV']
EXPORT_DIR      = ROOT/config['EXPORT_DIR']
ARCHIVE_DIR     = ROOT/config['ARCHIVE_DIR']
MAIN_CSV        = ROOT/config['MAIN_CSV']
# EXPORT_CSV      = ROOT/config['EXPORT_CSV']

ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
_DONE = {}

DATE_RE = re.compile(r"(\d{4})[-/]?(\d{1,2})[-/]?(\d{1,2})")

# Header Formats, what it expects to see.  modify if needed per import doc.
Date = "Date"
Action = "Action"
Qty = "Qty"
PricePerUnit = "PricePerUnit"
Notes = "Notes"
Fee = "Fee"

def safe_date(s):
    m = DATE_RE.match(s.strip())
    if not m: raise ValueError(s)
    # if not m:
    #     print("what")
    #     exit()
    y, m, d = map(int, m.groups())
    return datetime(y if y >= 100 else y + 2000, m, d)

# # this is supposed to be to archive pre-existing working files
def archive_old():
    today = datetime.now().strftime("%Y-%m-%d")
    for p in WORKING_DIR.glob("*.csv"):
        shutil.move(p, ARCHIVE_DIR / f"{p.stem}_{today}{p.suffix}")

# def import_transactions(method: str):
def import_transactions():
    src = IMPORT_CSV.resolve()
    if _DONE.get(src): return True, MAIN_CSV

    if not src.exists(): raise FileNotFoundError(src)

    backup = ARCHIVE_DIR / f"{src.stem}_{datetime.now().strftime('%Y%m%d_%H:%M:%S')}.csv" # ideal format?
    shutil.copy2(src, backup)

    with src.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # If the CSV file has no rows (empty file), the function immediately
    # returns True and the path to the main output CSV, skipping all processing.
    # It’s an early-exit so downstream code still receives a valid path even when there’s nothing to process.
    if not rows: return True, MAIN_CSV

    # add missing columns
    for r in rows:
        r.setdefault("Fee", "0")
        r.setdefault(Notes, "")

        qty = Decimal(r[Qty])
        px = Decimal(r[PricePerUnit])
        # fee = Decimal(r.get("Fee", "0"))  # does not contain a safe-cast, Decimal constructor will choke on empty str
        fee = Decimal (r.get("Fee", "0") or "0")
        # r["Notes"] = r["Notes"].strip()
        if r[Action].upper() == "BUY":
            r["CostBasis"] = str(qty * px + abs(fee))
        else:
            r["CostBasis"] = Decimal("0")

        if r[Action].upper() == "SELL":
            # assumes the fee will be absolute value
            r["Proceeds"] = str(qty * px + abs(fee))
        else:
            r["Proceeds"] = Decimal("0")

    date_sorted = sorted(rows, key=lambda r: safe_date(r["Date"]))
    # cost_sorted = sorted(rows, key=lambda r: Decimal(r["CostBasis"]), reverse=True)

    fields = ["Date", "Action", "Qty", "PricePerUnit", "Fee", "CostBasis", "Proceeds", "Notes"]
    # for path, data in [(MAIN_CSV, date_sorted), (MAIN_CSV, cost_sorted)]:
    for path, data in [(MAIN_CSV, date_sorted)]:
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fields)
            w.writeheader(); w.writerows(data)

    _DONE[src] = True
    return True, MAIN_CSV

def run():
    try:
        import_transactions()
        # print("Ready files", FIFO_LIFO_CSV, HIFO_CSV, sep="\n")
        print("Imports Formatted\n")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    run()
