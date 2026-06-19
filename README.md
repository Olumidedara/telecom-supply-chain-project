# Telecom Supply Chain & Sales Analysis

A comprehensive data analysis portfolio project examining **2,000 sales transactions** from a global telecommunications equipment supplier. The dataset spans **January 2023 to June 2025** and covers the full order-to-delivery lifecycle across 7 product categories, 15 suppliers, and 8 warehouses.

## Project Overview

| Aspect | Details |
|--------|---------|
| **Domain** | Telecommunications — Supply Chain & Sales |
| **Dataset** | 2,000 transactions, 24 columns |
| **Date Range** | Jan 2023 – Jun 2025 |
| **Tools** | Python, Pandas, Matplotlib, Seaborn, Jupyter |
| **Total Revenue** | $76.3M |
| **Total Profit** | $32.1M |
| **Overall Margin** | 42.1% |

## Repository Structure

```
telecom-supply-chain-portfolio/
├── data/
│   ├── generate_dataset.py          # Reproducible data generator
│   └── telco_supply_chain_sales.csv # Synthetic dataset (2000 records)
├── notebooks/
│   ├── telco_supply_chain_analysis.ipynb  # Jupyter notebook (recommended)
│   └── telco_supply_chain_analysis.py     # Standalone Python script
├── visuals/                         # Generated visualizations (PNG)
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## Dataset Description

The dataset includes the following fields:

| Column | Description |
|--------|-------------|
| `Order_ID` | Unique order identifier |
| `Order_Date` | Date the order was placed |
| `Delivery_Date` | Actual delivery date |
| `Product_Category` | Product type (7 categories) |
| `Product_Name` | Specific product model |
| `Quantity` | Units ordered |
| `Unit_Cost` | Cost per unit |
| `Unit_Price` | Selling price per unit |
| `Discount_Pct` | Discount percentage applied |
| `Revenue` | Total revenue (after discount) |
| `Total_Cost` | Total cost of goods |
| `Profit` | Revenue minus cost |
| `Profit_Margin_Pct` | Profit as percentage of revenue |
| `Lead_Time_Days` | Days from order to delivery |
| `Delivery_Status` | On Time / Delayed / Damaged / Cancelled |
| `Supplier_Name` | Supplier company |
| `Supplier_Region` | Asia / Europe / North America |
| `Warehouse_Location` | Fulfillment warehouse city |
| `Customer_Segment` | Enterprise / SME / Government / Individual |
| `Sales_Channel` | Direct / Online / Retail / Distributor / VAR |
| `Inventory_Level` | Current stock level |
| `Reorder_Point` | Minimum stock triggering reorder |
| `Safety_Stock` | Buffer stock level |

## How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate fresh dataset (optional — CSV is included)
cd data && python generate_dataset.py

# 3. Run the analysis
# Option A: Jupyter Notebook
jupyter notebook notebooks/telco_supply_chain_analysis.ipynb

# Option B: Python script
python notebooks/telco_supply_chain_analysis.py
```

## Key Findings (Executive Summary)

1. **Network Equipment** drives 43.3% of revenue and commands high margins (~43%). This is the core profit engine and should be prioritized across the supply chain.

2. **SIM Cards and Fiber Cables** have the highest margins (48–49%) but represent only 4.1% and 6.1% of revenue — a clear upsell opportunity.

3. **On-time delivery rate is 65%** — nearly one-third of orders experience delays or damage, putting ~$21M in revenue at risk.

4. **Direct Sales** channels deliver the best margins (47.8%) while **Retail Partners** lag at 35.5%. Channel mix optimization is needed.

5. **Asian suppliers** average 29-day lead times vs 22 days for Europe — a dual-sourcing strategy could reduce supply risk.

6. **Discounts above 15%** erode margins by ~15 percentage points. Tighter approval workflows are recommended.

7. **Government contracts** yield the highest segment margins (45.7%) and represent a strategic growth area.

## Visualizations

All charts are saved to the `visuals/` directory:

1. **Monthly Revenue & Order Volume Trend** — Bar + line combo chart
2. **Revenue by Product Category** — Ranked bar chart with percentage labels
3. **Top 10 Products by Revenue** — Horizontal bar chart
4. **Sales Channel Performance** — Pie chart + margin comparison
5. **Delivery Status Distribution** — Pie chart + revenue impact
6. **Lead Time Analysis** — By supplier region and product category
7. **Supplier Performance** — Dual-axis revenue vs on-time rate
8. **Profit Margins** — By customer segment and product category
9. **Discount Impact** — Margin erosion by discount bucket
10. **Segment–Channel Heatmaps** — Margin & revenue matrices
11. **Inventory Analysis** — Stock levels vs reorder points
12. **Warehouse Performance** — Revenue by fulfillment center
13. **Correlation Heatmap** — Key metric relationships
14. (and more in the full analysis)

## Recommendations

| # | Recommendation | Impact | Timeline |
|---|---------------|--------|----------|
| 1 | Supplier scorecard with lead-time SLAs for Asian suppliers | -30% lead time | Q3 |
| 2 | "Direct Sales Accelerator" program for Enterprise deals | +3-5% margin | Q3 |
| 3 | Discount approval workflow (>10% requires sign-off) | +2-3% margin | Immediate |
| 4 | Increase safety stock for Battery/Power products | +15% on-time | Q4 |
| 5 | Regional fulfillment centers near Atlanta, Dallas | -5-7d lead time | Q1 next |
| 6 | Bundle SIM/Fiber with Network Equipment orders | +8-12% revenue/order | Q4 |

## Methodology

- **Data Generation**: Synthetic dataset created with realistic distributions, seasonality patterns, and correlation structures modeled on real telecom industry benchmarks.
- **Analysis Approach**: Exploratory Data Analysis (EDA) with descriptive statistics, time-series trend analysis, segmentation, and correlation analysis.
- **Tools**: Python with Pandas for data manipulation, Matplotlib and Seaborn for visualization.

## License

MIT License

Copyright (c) 2026 Olumidedara

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

### ⭐ If you find this project useful, please give it a star!
