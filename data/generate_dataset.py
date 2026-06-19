"""
Telecom Supply Chain & Sales Dataset Generator
Generates realistic synthetic data for portfolio analysis project.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

NUM_RECORDS = 2000

products = {
    "Smartphones": [("Galaxy S24", 450, 799), ("iPhone 16", 550, 999), ("Pixel 9 Pro", 500, 899), ("OnePlus 13", 420, 749), ("Xiaomi 14 Pro", 380, 649)],
    "Network Equipment": [("5G Small Cell", 1200, 2200), ("Base Station BTS", 8500, 15000), ("Microwave Link", 3200, 5800), ("Fiber Optic Terminal", 600, 1100), ("Edge Router CR-5", 2100, 3800)],
    "SIM Cards": [("5G SIM eSIM", 0.50, 2.50), ("IoT M2M SIM", 0.80, 3.00), ("Prepaid SIM Kit", 0.30, 1.50), ("Roaming SIM Pro", 1.20, 5.00), ("Enterprise Multi-IMSI", 2.00, 8.00)],
    "Fiber Cables": [("Single-Mode OS2 1km", 55, 120), ("Multi-Mode OM4 1km", 40, 95), ("Armored Drop Cable", 25, 60), ("Indoor Patch Cord 3m", 3, 8), ("ADSS Cable 1km", 70, 150)],
    "Routers & Gateways": [("Home Gateway HG-1", 25, 65), ("WiFi 7 Mesh Router", 60, 150), ("Industrial IoT Gateway", 180, 390), ("SD-WAN Appliance", 400, 850), ("Enterprise Core Router", 2800, 5200)],
    "Antennas": [("Omni 5G Antenna", 80, 190), ("Directional Panel Antenna", 120, 280), ("Massive MIMO Array", 2500, 4800), ("DAS Indoor Antenna", 35, 85), ("Parabolic Dish 0.6m", 150, 320)],
    "Batteries & Power": [("Lithium Backup 48V", 320, 580), ("Tower Power Cabinet", 1800, 3200), ("Small Cell UPS", 450, 820), ("Solar Panel 500W", 400, 720), ("Battery Rack 48V 100Ah", 900, 1600)],
}

suppliers = {
    "Asia": ["Samsung Networks", "Huawei Tech", "ZTE Corp", "Foxconn Telecom", "Honor Devices"],
    "Europe": ["Ericsson AB", "Nokia Solutions", "Siemens Networks", "Alcatel-Lucent", "Cobham Wireless"],
    "North America": ["Cisco Systems", "Qualcomm Supply", "CommScope Inc", "Juniper Networks", "Corning Optical"],
}

warehouses = ["Atlanta, GA", "Dallas, TX", "Los Angeles, CA", "Chicago, IL", "Newark, NJ", "Miami, FL", "Denver, CO", "Seattle, WA"]
customer_segments = ["Enterprise", "SME", "Government", "Individual"]
sales_channels = ["Direct Sales", "Online Portal", "Retail Partner", "Distributor", "Value-Added Reseller"]

records = []
start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 6, 1)

for i in range(1, NUM_RECORDS + 1):
    cat = random.choice(list(products.keys()))
    prod_name, unit_cost, unit_price = random.choice(products[cat])
    qty = random.choices(
        [1, 2, 5, 10, 25, 50, 100, 200, 500, 1000],
        weights=[25, 20, 15, 12, 10, 7, 5, 3, 2, 1]
    )[0]

    discount_pct = 0
    if random.random() < 0.35:
        discount_pct = random.choice([5, 10, 15, 20, 25])

    final_price = unit_price * (1 - discount_pct / 100)
    revenue = round(qty * final_price, 2)
    cost = round(qty * unit_cost, 2)
    profit = round(revenue - cost, 2)

    region = random.choice(list(suppliers.keys()))
    supplier = random.choice(suppliers[region])
    warehouse = random.choice(warehouses)
    segment = random.choice(customer_segments)
    channel = random.choice(sales_channels)

    order_date = start_date + timedelta(
        days=random.randint(0, (end_date - start_date).days)
    )

    base_lead_time = random.randint(2, 45)
    if "Fiber" in cat or "Antenna" in cat:
        base_lead_time += random.randint(5, 15)
    if region == "Asia":
        base_lead_time += random.randint(3, 10)
    elif region == "Europe":
        base_lead_time += random.randint(1, 5)

    if channel == "Direct Sales":
        base_lead_time = max(1, base_lead_time - random.randint(1, 5))
    if segment == "Enterprise" or segment == "Government":
        base_lead_time += random.randint(2, 8)

    delivery_date = order_date + timedelta(days=base_lead_time)

    delay_prob = random.random()
    if delay_prob < 0.65:
        status = "On Time"
    elif delay_prob < 0.85:
        status = "Delayed"
        delivery_date += timedelta(days=random.randint(3, 20))
    elif delay_prob < 0.94:
        status = "Damaged"
        delivery_date += timedelta(days=random.randint(5, 30))
    else:
        status = "Cancelled"
        delivery_date = pd.NaT

    if status == "On Time":
        lead_time = base_lead_time
    elif status == "Delayed" or status == "Damaged":
        lead_time = (delivery_date - order_date).days if pd.notna(delivery_date) else base_lead_time
    else:
        lead_time = base_lead_time

    inventory_level = random.randint(0, max(500, qty * 3))
    reorder_point = random.randint(20, max(50, qty * 2))
    safety_stock = random.randint(10, max(30, qty))

    records.append({
        "Order_ID": f"ORD-{i:05d}",
        "Order_Date": order_date.strftime("%Y-%m-%d"),
        "Delivery_Date": delivery_date.strftime("%Y-%m-%d") if pd.notna(delivery_date) else "",
        "Product_Category": cat,
        "Product_Name": prod_name,
        "Quantity": qty,
        "Unit_Cost": unit_cost,
        "Unit_Price": unit_price,
        "Discount_Pct": discount_pct,
        "Revenue": revenue,
        "Total_Cost": cost,
        "Profit": profit,
        "Profit_Margin_Pct": round((profit / revenue) * 100, 2) if revenue > 0 else 0,
        "Lead_Time_Days": lead_time,
        "Delivery_Status": status,
        "Supplier_Name": supplier,
        "Supplier_Region": region,
        "Warehouse_Location": warehouse,
        "Customer_Segment": segment,
        "Sales_Channel": channel,
        "Inventory_Level": inventory_level,
        "Reorder_Point": reorder_point,
        "Safety_Stock": safety_stock,
    })

df = pd.DataFrame(records)

csv_path = "telco_supply_chain_sales.csv"
df.to_csv(csv_path, index=False)
print(f"Dataset generated: {len(df)} records -> {csv_path}")
print(f"Columns: {list(df.columns)}")
print(f"Date range: {df['Order_Date'].min()} to {df['Order_Date'].max()}")
print(f"Total Revenue: ${df['Revenue'].sum():,.2f}")
print(f"Total Profit: ${df['Profit'].sum():,.2f}")
print(f"Overall Margin: {df['Profit'].sum()/df['Revenue'].sum()*100:.1f}%")
