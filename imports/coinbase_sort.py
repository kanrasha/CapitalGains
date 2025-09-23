import csv
from decimal import Decimal

input_csv = "Coinbase-2024-CB-GAINLOSSCSV.csv"

short_term = []
long_term = []

with open(input_csv, mode="r") as f:
    reader = list(csv.DictReader(f))

    for row in reader:
        a = row["Transaction Type"]
        b = row["Transaction ID"]
        c = row["Tax lot ID"]
        d = row["Asset name"]
        e = row["Amount"]
        f = row["Date Acquired"]
        g = row["Cost basis (USD)"]
        h = row["Date of Disposition"]
        i = row["Proceeds (USD)"]
        gains = Decimal(row["Gains (Losses) (USD)"])
        term = int(row["Holding period (Days)"])
        data_source = row["Data source"]

        if term <= 365:
            short_term.append(gains)
        elif term > 365:
            long_term.append(gains)

    short_term_gains = round(sum(g for g in short_term),2)
    long_term_gains = round(sum(g for g in long_term),2)

# PRINTOUT
print(data_source[:], "PNL (FIFO)")
print("Short Term $"+str(short_term_gains), "|", "Long Term $"+str(long_term_gains))
print("Total = $"+str(short_term_gains+long_term_gains))

