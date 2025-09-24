"""
4.2 UPDATE (TO DO):
- AddEXPORT_DIR.mkdir(exist_ok=True) to your code so your program is resilient and never fails due to a missing directory, no matter how the user obtained or modified the files.
- in export, add "PurchasePricePerUnit"
- there needs to be 3 unique export files for each accounting method
- improve GUI
- any-file import (at least space tolerant) - this should be a file prep update
- delete archived working file after the checksum passes
- create new file for global constants such as BASE, ARCHIVE_DIR, etc (?)
- what kinds of logs may be needed for better record keeping
- multiple asset handling (file_import)
- file format compatibility for Coinbase, Gemini, Kraken, Binance
- for later? wash sale prevention for stocks, with a flag that it has happened, and to how much $
- remove any old archived files (file_prep) after the formatting has been completed
- study and filter unnecessary (for example, unused references in checksum function)
- import and export transactions need a sort of txid (date, action, qty, source)
so that they can be matched up again with repeat imports, particularly full data sets which have already
been partly accounted for.  Let's call it "tax mode" with a one-year-selection scope, while "historical mode"
provides a full computation or multiple years.  Either way, the one year view will need to dive back into
transactions that may have already been accounted for on previous tax returns, and the original file may not
be markable with that info.
- make sure all export files are archived on every run (add process code? maybe not needed)

COMPLETED:
- formatted and improved the final printout, including location for export file
- there was an inappropriate reuse of the file_prep's term "IMPORT_CSV", changed to MAIN_CSV
- changed "BASE" to "ROOT" to match file_prep terminology
- modified GUI for an option to present all 3 accounting methods at once

8/23/25
"""

import file_prep0_3; file_prep0_3.run()

import csv, yaml
from datetime import datetime
from pathlib import Path
from decimal import Decimal

with open('paths.yaml', 'r') as f:
    config = yaml.safe_load(f)

ROOT            = Path(__file__).parent
ARCHIVE_DIR     = ROOT/config['ARCHIVE_DIR']
MAIN_CSV        = ROOT/config['MAIN_CSV']
# EXPORT_CSV      = ROOT/config['EXPORT_CSV']
EXPORT_DIR      = ROOT/config['EXPORT_DIR']

def capgains(method: str):
    EXPORT_CSV = ROOT / config['EXPORT_DIR'] / f"capital_gains_{method}.csv"
    EXPORT_DIR.parent.mkdir(parents=True, exist_ok=True)

    buys = []
    sells = []
    gains = []
    bag = Decimal("0")

    src = MAIN_CSV
    with src.open(newline="", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    for row in reader:
        qty        = Decimal(row["Qty"])
        price      = Decimal(row["PricePerUnit"])
        fee        = Decimal(row.get("Fee", "0") or "0")
        date       = datetime.strptime(row["Date"], "%Y-%m-%d")
        cost_basis = Decimal(row.get("CostBasis", "0") or "0")
        proceeds   = Decimal(row.get("Proceeds", "0") or "0")

        if row["Action"].upper() == "BUY":
            buys.append([date, qty, cost_basis, price])
            bag += qty

        elif row["Action"].upper() == "SELL":
            sells.append([date, qty, price, proceeds, fee])
            bag -= qty
            rem = qty
            sell_price = price
            # cost_total = Decimal("0")
            queue = (
                sorted(buys, key=lambda x: x[2], reverse=True)  # HIFO
                if method == "hifo"
                else buys[::-1] if method == "lifo"
                else buys  # FIFO
            )

            while rem and queue:
                buy_date, buy_qty, buy_cost, buy_price = queue[0]
                used = min(rem, buy_qty)
                cost_basis_slice = used * buy_price
                queue[0][1] -= used

                if queue[0][1] == 0:
                    queue.pop(0)
                rem -= used
                holding_days = (date - buy_date).days
                term = "Short" if holding_days <= 365 else "Long"

                gains.append({
                    "DateSold": row["Date"],
                    "DatePurchased": buy_date.strftime("%Y-%m-%d"),
                    "QtySold": str(used),
                    "SalePricePerUnit": str(price),
                    "TotalSaleProceeds": round((used * sell_price),2),
                    "TotalCostBasis": round((cost_basis_slice),2),
                    "CapitalGain": round(((used * sell_price) - (cost_basis_slice)),2),
                    "Fee": round(fee,2),
                    "Term": term,
                    "HoldingDays": holding_days
                })

    # export
    if not gains:
        print("No sells to process or IndexError from import file header mismatch")
        return

    with EXPORT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=gains[0].keys())
        writer.writeheader()
        writer.writerows(gains)

    short_total = sum(Decimal(g["CapitalGain"]) for g in gains if g["Term"] == "Short")
    long_total  = sum(Decimal(g["CapitalGain"]) for g in gains if g["Term"] == "Long")
    print(method.upper())
    print(f"Short: ${short_total:+,.2f}  "
          f"|  Long: ${long_total:+,.2f}  "
          f"|  Total: ${short_total+long_total:+,.2f}  "
          f"|  Remaining: {bag:.8f}\n")
    # print("\n")
    # print(f"Remaining: {bag:.8f}")

def checksum():
    """
    1. Re-compute unit price from export and compare to import.
    2. Verify total BTC bought - total BTC sold == remaining bag.
    Prints PASS / FAIL and exits with 0 or 1.
    """

    # ---------- 1. Price-consistency ----------
    # export_rows = []
    method_tag = ["FIFO", "LIFO", "HIFO"]

    for tag in method_tag:
        try:
            EXPORT_CSV = ROOT / config["EXPORT_DIR"] / f"capital_gains_{tag.upper()}.csv"

            with EXPORT_CSV.open(newline="", encoding="utf-8") as f:
                export_rows = list(csv.DictReader(f))

            # unit price from export
            export_unit_prices = [Decimal(r["SalePricePerUnit"]) for r in export_rows]

            # unit price from import
            # import_rows = []
            with MAIN_CSV.open(newline="", encoding="utf-8") as f:
                import_rows = list(csv.DictReader(f))

            import_unit_prices = [Decimal(r["PricePerUnit"]) for r in import_rows]

            # simple checksum: every export unit price must appear in import
            price_ok = all(up in import_unit_prices for up in export_unit_prices)

            # ---------- 2. Running-balance ----------
            total_bought = sum(Decimal(r["Qty"]) for r in import_rows if r["Action"].upper() == "BUY")
            total_sold   = sum(Decimal(r["Qty"]) for r in import_rows if r["Action"].upper() == "SELL")
            bag_from_import = total_bought - total_sold

            # remaining from program
            bag_from_program = Decimal("0")
            for row in import_rows:
                qty = Decimal(row["Qty"])
                if row["Action"].upper() == "BUY":
                    bag_from_program += qty
                else:
                    bag_from_program -= qty

            balance_ok = bag_from_program == bag_from_import

            # ---------- report ----------
            print(f"CHECKSUM for {tag}:",
                  f"[Price Consistency: {'OK]' if price_ok else 'FAIL]'} "
                  f"[Running Balance: {'OK]' if balance_ok else 'FAIL]'}")
            print("EXPORT:", EXPORT_CSV.resolve())
            # if price_ok and balance_ok:
            #     backup.unlink(missing_ok=True)  # delete archived file
            if not (price_ok and balance_ok):
                exit(1)
        except:
            pass

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", choices=["fifo", "lifo", "hifo"], default="fifo")
    args = parser.parse_args()
    capgains(args.method); print(f'FUTURE: Remaining: ______ print out one time here instead of per method')
    checksum()