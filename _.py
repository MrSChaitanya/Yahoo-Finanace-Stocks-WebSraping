import time
import os
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ----- CONFIGURATION & SETUP -----
options = webdriver.ChromeOptions()
# 'eager' ignores background ad pixels, executing as soon as basic layout is interactive
options.page_load_strategy = 'eager' 

driver = webdriver.Chrome(options=options)
driver.maximize_window()

wait = WebDriverWait(driver, 15)

# Target URL for Yahoo's Most Active Stocks page
url = "https://finance.yahoo.com/markets/stocks/most-active/"
print(f"Opening data source URL: {url}")
driver.get(url)

# Give data-heavy components an explicit short window to settle down visually
time.sleep(5)

data = []
page_number = 1

# ----- CLEAN & SECURE DATA EXTRACTION LOOP -----
while True:
    try:
        print(f"Extracting stock rows from page {page_number}...")
        
        # Explicitly wait for table container rows to display fully on-screen
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "table tbody tr")))
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        
        print(f"Found {len(rows)} data rows on page {page_number}.")
        
        for row in rows:
            try:
                values = row.find_elements(By.TAG_NAME, "td")
                
                # Yahoo Finance uses ~10 data attributes per entry
                if len(values) < 6:
                    continue
                
                # --- CRITICAL FIX FOR YAHOO CELL SPLITTING ---
                # Cell 0 contains both symbol and name stacked together. 
                # We split them cleanly using newline separation techniques.
                raw_symbol_cell = values[0].text.strip()
                cell_lines = raw_symbol_cell.split('\n')
                
                symbol = cell_lines[0] if len(cell_lines) > 0 else "N/A"
                name = cell_lines[1] if len(cell_lines) > 1 else symbol
                
                stock = {
                    "symbol": symbol,
                    "name": name,
                    "price": values[1].text.strip(),
                    "change": values[2].text.strip(),
                    "volume": values[5].text.strip() if len(values) > 5 else "0",
                    "market_cap": values[6].text.strip() if len(values) > 6 else "0",
                    "pe_ratio": values[7].text.strip() if len(values) > 7 else "-"
                }
                data.append(stock)
            except Exception as cell_err:
                # Keeps the processing stream running if a single row has an extraction hitch
                continue

        # --- PAGINATION NAVIGATION ENGINE ---
        try:
            # Direct target structure lookup pointing to the Next navigation button
            next_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Next"] | //span[text()="Next"]/parent::button'))
            )
            
            # Stop sequence if button is marked visually dead or unclickable
            if not next_button.is_enabled() or "disabled" in next_button.get_attribute("class"):
                print("End of dataset pagination reached.")
                break
                
            next_button.click()
            page_number += 1
            time.sleep(3) # Yield for internal table content refresh calls
            
        except Exception:
            print("No viable pagination 'Next' node detected. Scraping loop terminated.")
            break

    except Exception as e:
        print(f"Extraction halted prematurely due to structural change: {e}")
        break

# Gracefully release system assets 
driver.quit()

# ----- DATA CLEANING & PERMANENT STORAGE EXPORT -----
if data:
    print(f"Scraped {len(data)} total entries. Structuring Pandas dataframe...")
    
    # Generate structured dataset frame object mapping
    df = pd.DataFrame(data)
    
    # Dynamic text removal and element normalization mappings
    df['price'] = pd.to_numeric(df['price'].str.replace(",", "", regex=False), errors='coerce')
    df['change'] = pd.to_numeric(df['change'].str.replace("+", "", regex=False).str.replace("%", "", regex=False).str.replace(",", "", regex=False), errors='coerce')
    
    # Normalize Volume structures containing 'M' metrics smoothly
    df['volume'] = df['volume'].apply(lambda val: float(str(val).replace("M", "").replace(",", "")) if "M" in str(val) else (float(str(val).replace("B", "").replace(",", "")) * 1000 if "B" in str(val) else pd.to_numeric(val, errors='coerce')))
    
    # Handle multi-tier billions/trillions tracking string evaluations seamlessly
    df['market_cap'] = df['market_cap'].apply(lambda val: float(str(val).replace("B", "").replace(",", "")) if "B" in str(val) else (float(str(val).replace("T", "").replace(",", "")) * 1000 if "T" in str(val) else pd.to_numeric(val, errors='coerce')))
    df['pe_ratio'] = pd.to_numeric(df['pe_ratio'].replace("-", np.nan).str.replace(",", "", regex=False), errors='coerce')
    
    # Align structural export clean names
    df = df.rename(columns={
        "price": "price_usd",
        "volume": "volume_M",
        "market_cap": "market_cap_B"
    })
    
    # Force immediate verification check across local target folders
    output_filename = "yahoo-stocks-data.xlsx"
    target_path = os.path.abspath(output_filename)
    
    df.to_excel(output_filename, index=False)
    print(f"\n SUCCESS! Spreadsheet file created out.")
    print(f"Target Save Directory Absolute Path:\n--> {target_path}")
else:
    print("\n Data pipeline ran empty. No file was output to your directory.")
