# 📱 Smartphone Market Analysis

### End-to-end data pipeline and analysis of 5G smartphones priced above ₹20,000, exploring brand trends, price-performance dynamics, and value-for-money insights using Python, Pandas, and Matplotlib.

---

## 🚀 Project Overview
This project analyzes the **5G smartphone market in India** to uncover:
- Which brands dominate various price segments  
- How specifications (RAM, storage, camera, etc.) scale with price  
- Which models offer the **best value for money**  
- How premium pricing often leads to **diminishing returns**

The dataset was **web-scraped from Flipkart** using Selenium and BeautifulSoup, then cleaned, combined, scored, and analyzed using a reproducible Python pipeline.

---

## 🧱 Tech Stack

| Category | Tools Used |
|-----------|-------------|
| **Data Scraping** | Selenium, BeautifulSoup, WebDriverManager |
| **Data Processing** | Python, Pandas |
| **Data Storage** | JSON (raw), CSV / Parquet (clean), CSV (processed) |
| **Visualization** | Matplotlib |
| **Automation** | Custom pipeline scripts (`clean_data.py`, `combine_data.py`, `run_pipeline.py`) |
| **Environment** | Jupyter Notebook |

---

## 📁 Folder Structure

'''
Mobile_Phones_Analysis/
│
├─ analysis/ # PNG charts and visualizations
│ └─ figures/
│
├─ data/
│ ├─ raw/ # Scraped JSON dumps
│ ├─ clean/ # Cleaned brand-level CSVs
│ └─ processed/ # Final combined & scored dataset
│
├─ pipeline/
│ ├─ clean_data.py # Cleans all raw JSON files
│ ├─ combine_data.py # Combines all cleaned CSVs
│ └─ run_pipeline.py # Automates the full data flow
│
├─ utils/
│ └─ Scoring.py # Scoring logic (composite + value-per-rupee)
│
├─ 01_market_landscape_segment_dominance.ipynb
├─ 02_brand_dominance_across_segments.ipynb
├─ 03_price_spec_correlation.ipynb
├─ 04_brand_spec_bias.ipynb
├─ 05_hardware_value_index.ipynb
├─ 06_flagship_inflation_diminishing_returns.ipynb
└─ README.md
'''


---

## 🔁 Data Pipeline Overview

| Stage | Description |
|--------|-------------|
| **1. Scraping** | Individual brand scrapers fetch smartphone listings (≥ ₹20,000) with key specs. |
| **2. Cleaning** | Removes noise, extracts numeric fields (RAM, storage, battery, camera, display). |
| **3. Combining** | Merges brand-level data into one master dataset. |
| **4. Scoring** | Applies composite & value-per-rupee formulas. |
| **5. Analysis** | Generates visual and statistical insights across six analytical notebooks. |

---

## 🧮 Scoring Formula

A **composite scoring function** was designed to measure overall hardware performance:

\[
\text{Composite Score} = (3 \times RAM) + \frac{Storage}{64} + \frac{Battery}{1500} + \frac{Camera_{MP}}{12} + (Display_{inch} \times 0.5)
\]

Value-for-money was calculated as:

\[
\text{Value per 100k Rupees} = \frac{\text{Composite Score}}{\text{Price}} \times 100000
\]

---

## 📊 Key Insights

- **₹20–30k** range dominates the 5G market (~67% of models).  
- **Realme** and **Xiaomi** consistently offer the best value efficiency.  
- **Samsung** leads in overall model count and premium presence.  
- **Display size** and **battery capacity** show weak correlation with price — most models stay in the 6.3–6.8” / 5000–6000mAh range.  
- Above ₹60k, phones show **diminishing value returns**, emphasizing brand and ecosystem premium.

---

## 🧩 Highlighted Notebooks

| Notebook | Focus Area |
|-----------|-------------|
| `01_market_landscape_segment_dominance.ipynb` | Market overview and price segmentation |
| `02_brand_dominance_across_segments.ipynb` | Brand share by price range |
| `03_price_spec_correlation.ipynb` | Correlations between specs and price |
| `04_brand_spec_bias.ipynb` | How brands prioritize specs differently |
| `05_hardware_value_index.ipynb` | Value-for-money analysis using composite score |
| `06_flagship_inflation_diminishing_returns.ipynb` | Decline in value efficiency at premium tiers |

---

## ⚙️ How to Reproduce

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/smartphone_market_analysis.git
   cd smartphone_market_analysis
