# Stock Prices Web Scraper 📈

A modular Python-based web scraper that automatically extracts live or historical stock data from Yahoo Finance and exports it into a clean, structured Excel spreadsheet.

This project is built using **Selenium** to handle dynamic JavaScript-rendered content and **Pandas** for vectorized data cleaning and transformation.

---

## 🚀 Features

* **Dynamic Data Extraction:** Bypasses JavaScript-heavy layouts on Yahoo Finance to capture accurate real-time stock metrics.
* **Automated Data Pipeline:** Cleans up raw numbers, handles formatting irregularities, and processes financial text into structured values.
* **Multi-Format Architecture:** Includes both a straightforward monolithic script (`stocks-scraper.py`) and a clean, production-grade restructured version (`restructured-stocks-scraper.py`).
* **Excel Export:** Automatically aggregates the scraped data into a pristine spreadsheet (`yahoo_finance-stocks.xlsx`) for instant analysis.

---

## 🛠️ Tech Stack & Prerequisites

Before running the scraper, ensure you have the following installed:

* **Python 3.8+**
* **Google Chrome Browser** (and the matching ChromeDriver version managed automatically)

### Dependencies
Install the required Python packages using `pip`:

```bash
pip install selenium pandas numpy openpyxl
```
---
## 📂 Project Structure

```text
Stock Prices/
│
├── stocks-scraper.py               # Monolithic standalone scraping script
├── restructured-stocks-scraper.py  # Optimized/modular version of the scraper
├── requirements.txt                # Project dependencies configuration file
├── README.md                       # Documentation and project guide
└── yahoo_finance-stocks.xlsx       # Final cleaned output data sheet
```
---

## 💻 How to Run
Clone or navigate to your local project directory.

Run either version of the script using your terminal:

To run the standard scraper:
```bash
python "stocks-scraper.py"
```
To run the production-ready modular scraper:
```bash
python "restructured-stocks-scraper.py"
```
---

## 📊 Data Pipeline Details

The scraper navigates to the target stock page, waits for the dynamic elements to load securely, and extracts the following fields:

* **Ticker Symbol / Company Name**
* **Stock Price** (Stripped of local currency symbols and formatted as floats)
* **Price Movements / Percentage Changes**
* **Trading Volumes**

The Pandas data-cleaning pipeline automatically drops duplicates, handles missing (`NaN`) values gracefully, ensures proper data type casting, and standardizes column headers before saving to Excel.




