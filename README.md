# 🟪 Capital Gains Calculator
Designed to work offline and with client side data custody.  Open source project.

## What It Does
A single `.csv` → clean gain/loss tables (short & long) and remaining inventory.
To run the program, just run the GUI script.  There is an example CSV in place for demonstration.

## Input File Format
**`transactions.csv`:** Date, Action, Quantity, PricePerUnit, Notes (optional), Fee* (optional) <br>
*Fee column is optional as far as the script is concerned, but it is required if the price does not account for the fee*
- Source file:   imports/transactions.csv
- Clean copy:    working_files/transactions_formatted.csv
- Export:        exports/capital_gains.csv
- IRS Exports:    *this has not been made yet, but they will be formatted properly for IRS Form 8949 and Schedule D*

## Quick Start
- Download the zip
- 1: Put your CSV into imports/
- 2: Run python capgains.py (or the GUI) <br><br>
- If running the individual scripts, user must customize the paths at the top so that **`capgains[version#].py`** can locate the **`file_prep[version#].py`** script, and again for `file_prep` so that it can locate the import csv.

## Accounting Methods (toggle in settings)

- FIFO – First In First Out: first units bought are first sold (default IRS).
- LIFO – Last In First Out: newest units sold first (may shift gains to long-term).
- HIFO – Highest In First Out: highest-cost units sold first (minimizes immediate tax).

## Additional Accounting Methods Allowed by the IRS (yet to be implemented here)
- Specific-ID (Spec-ID): this is the actual 8949 implementation of LIFO or HIFO, but can be more specific
- Average Basis Method (Average Cost): This is only allowed for mutual fund shares, and not applicable here.

# ⬜ Compare Capital Gains Tools
*This may not be the latest information, updated last on 9/22/25*

<br>

## 🟢 This Program (Yet To Be Named)
| Service | Starting Cost | Tx Limit | Methods | Free Tax Docs | Free CSV | Paid Docs | Notes |
|---|---|---|---|---|---|---|---|
| HakoLabs | $0 | none | FIFO/LIFO/HIFO | 8949, Schedule D, 1099-B, 1099-B summary (soon) | gain/loss CSV | — | offline / desktop install, no limits, customizable, wash sale flags (one day) |


## 🟢 Capital Gains Tools in Consumer Tax Software
*You can use them as a "black box" calculator to see the final number, but you cannot get the generated forms out of the system without paying the full price for that software tier.*<br>
***Note:** Prices are approximate for the 2024 online filing season and typically increase as the deadline approaches. State filing is an additional fee.*
| Software | Tier | Federal Cost (Approx. USD) | State Cost (Approx. USD) | Handles Raw CSV? | Crypto Support | Notes |
|---|---|---|---|---|---|---|
| **TurboTax** | Premier | $99 - $129 | ~$59 | Yes | Direct import from major exchanges and partners like CoinTracker | Best for direct API import from hundreds of brokers. |
| **TurboTax** | Self-Employed | $129 - $219 | ~$59 | Yes | Direct import from major exchanges and partners like CoinTracker | Includes all Premier features plus business/1099-NEC tools. |
| **H&R Block** | Deluxe | $55 - $85 | ~$45 | Yes | Direct import from major exchanges and partners | Lower-cost tier that still handles stocks/crypto. |
| **H&R Block** | Premium | $75 - $115 | ~$45 | Yes | Direct import from major exchanges and partners | Includes all Deluxe features plus rental property/Schedule E. |
| **TaxAct** | Premier+ | $69 - $99 | ~$59 | Yes | Has its own built-in crypto import tool for major exchange CSVs | A budget-friendly alternative for standard stock/crypto filing. |
| **TaxAct** | Self-Employed+ | $99 - $159 | ~$59 | Yes | Has its own built-in crypto import tool for major exchange CSVs | Includes all Premier+ features plus business/freelance tools. |


## 🔴 Enterprise Software
| Service | Starting Cost | Tx Limit | Methods | Tax Docs | CSV | Notes |
|---|---|---|---|---|---|---|
| TaxAct Pro | $600-1,300 | none | FIFO/LIFO/HIFO | 1099-B summary | gain/loss CSV | desktop install |
| ProSeries | $1,400-3,400 | none | FIFO/LIFO/HIFO | 1099-B summary | gain/loss CSV | desktop install |
| Drake Tax | $1,795 | none | FIFO/LIFO/HIFO | 1099-B summary | gain/loss CSV | desktop install |
| Lacerte | $3k-6k | none | FIFO/LIFO/HIFO | 1099-B summary | gain/loss CSV | desktop install |
| UltraTax CS | $4k-8k | none | FIFO/LIFO/HIFO | 1099-B summary | gain/loss CSV | desktop install |
| ProSystem fx Tax | $6k-10k+ | none | FIFO/LIFO/HIFO | 1099-B summary | gain/loss CSV | enterprise |
| GoSystem RS | $8k-12k+ | none | FIFO/LIFO/HIFO | 1099-B summary | gain/loss CSV | cloud or local |


## 🔴 Traditional Brokers
| Service | Starting Cost | Tx Limit | Methods | Free Tax Docs | Free CSV | Paid Docs | Notes |
|---|---|---|---|---|---|---|---|
| Charles Schwab | $0 | ≤100 | FIFO | 1099-B summary | — | $50 raw CSV w/ full 1099-B |  |
| Merrill Edge | $0 | ≤100 | FIFO | 1099-B summary | — | $50 raw CSV w/ full 1099-B |  |
| E*Trade | $0 | ≤100 | FIFO | 1099-B summary | — | $50 raw CSV w/ full 1099-B |  |
| TD Ameritrade | $0 | ≤100 | FIFO | 1099-B summary | — | $50 raw CSV w/ full 1099-B |  |
| Fidelity | $0 | ≤100 | FIFO | 1099-B summary | — | $50 raw CSV w/ full 1099-B |  |
| Vanguard | $0 | ≤100 | FIFO | 1099-B summary | — | $50 raw CSV w/ full 1099-B |  |
| Interactive Brokers | $0 | none | FIFO | 1099-B summary | raw CSV | — | always full 1099-B + CSV |

## 🔴 Crypto
| Service | Starting Cost | Tx Limit | Methods | Free Tax Docs | Free CSV | Paid Docs | Notes |
|---|---|---|---|---|---|---|---|
| Coinbase | $0 | none | FIFO | 1099-B summary | raw CSV | — | — |
| Gemini | $0 | none | FIFO | 1099-B summary | raw CSV | — | — |
| Kraken | $0 | none | FIFO | 1099-B summary | raw CSV | — | — |
| Binance.US | $0 | none | FIFO | 1099-B summary | raw CSV | — | — |
| Crypto.com App | $0 | none | FIFO | 1099-B summary | raw CSV | — | — |
| CashApp | $0 | none | FIFO | 1099-B summary | — | — | raw CSV |
| PayPal | $0 | none | FIFO | 1099-B summary | — | — | no CSV option |
| Venmo | $0 | none | FIFO | 1099-B summary | — | — | no CSV option |
| BlockFi | $0 | none | FIFO | 1099-B summary | raw CSV | — | — |
| Uphold | $0 | none | FIFO | 1099-B summary | raw CSV | — | — |
| Bitstamp | $0 | none | FIFO | 1099-B summary | raw CSV | — | — |
| CoinTracker Free | $0 | ≤25 | FIFO | 1099-B summary | raw CSV | — | 1 wallet/exchange limit |
| CoinTracker Hobbyist | $60 | ≤100 | FIFO/LIFO/HIFO | 1099-B summary | — | gain/loss CSV | unlimited wallets |
| CoinTracker Investor | $199 | ≤1000 | FIFO/LIFO/HIFO | 1099-B summary | — | gain/loss CSV | TurboTax/TaxAct import |
| CoinTracker Pro | $599 | ≤3000 | FIFO/LIFO/HIFO | 1099-B summary | — | gain/loss CSV | CPA review |
| CoinTracker Unlimited | $999 | none | FIFO/LIFO/HIFO | 1099-B summary | — | gain/loss CSV | priority support |
| Koinly Free | $0 | ≤25 | FIFO | 1099-B summary | manual CSV | — | 1 wallet/exchange |
| Koinly Hobbyist | $59 | ≤100 | FIFO/LIFO/HIFO | 1099-B summary | gain/loss CSV | — | unlimited wallets |
| Koinly Investor | $199 | ≤1,000 | FIFO/LIFO/HIFO | 1099-B summary | gain/loss CSV | — | TurboTax/TaxAct import |
| Koinly Pro | $599 | ≤3,000 | FIFO/LIFO/HIFO | 1099-B summary | gain/loss CSV | — | CPA review |
| Koinly Unlimited | $999 | none | FIFO/LIFO/HIFO | 1099-B summary | gain/loss CSV | — | priority support |


## 🔴 Fintech (Hybrid Brokers)
| Service | Starting Cost | Tx Limit | Methods | Free Tax Docs | Free CSV | Paid Docs | Notes |
|---|---|---|---|---|---|---|---|
| Robinhood | $0 | ≤100 | FIFO | 1099-B summary | raw CSV | — | — |
| Robinhood Tax Doc Service | $50-100 | none | FIFO | 1099-B summary | — | raw CSV, 1099-B | paid tier only |
| Webull | $0 | none | FIFO | 1099-B summary | raw CSV | — | — |
| Ally Invest | $0 | none | FIFO | 1099-B summary | raw CSV | — | — |
| Public.com | $0 | none | FIFO | 1099-B summary | raw CSV | — | — |
| eToro US | $0 | none | FIFO | 1099-B summary | raw CSV | — | — |
| SoFi | $0 | none | FIFO | 1099-B summary | raw CSV | — | — |
| Dave | $0 | none | FIFO | 1099-B summary | — | — | no CSV option |

## 🔴 Wallets
| Service | Starting Cost | Tx Limit | Methods | Free Tax Docs | Free CSV | Paid Docs | Notes |
|---|---|---|---|---|---|---|---|
| MetaMask | $0 | none | none | — | raw CSV | — | non-custodial |
| Phantom | $0 | none | none | — | raw CSV | — | non-custodial |
| Exodus | $0 | none | none | — | raw CSV | — | non-custodial |
| Trust Wallet | $0 | none | — | — | raw CSV | — | non-custodial |
