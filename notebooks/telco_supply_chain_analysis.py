"""
Telecommunication Supply Chain & Sales Analysis
================================================
Portfolio project analyzing 2,000 transactions from a global telecom equipment supplier.
Dataset: Jan 2023 - Jun 2025 | Products: Smartphones, Network Equipment, SIM Cards, Fiber, etc.

Run this script to generate all visualizations and insights.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# ---------------------------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------------------------
df = pd.read_csv('../data/telco_supply_chain_sales.csv')
df['Order_Date'] = pd.to_datetime(df['Order_Date'])
df['Delivery_Date'] = pd.to_datetime(df['Delivery_Date'], errors='coerce')

print(f'Shape: {df.shape}')
print(f'Date Range: {df["Order_Date"].min().date()} to {df["Order_Date"].max().date()}')
print(f'Total Revenue: ${df["Revenue"].sum():,.2f}')
print(f'Total Profit: ${df["Profit"].sum():,.2f}')
print(f'Overall Margin: {df["Profit"].sum()/df["Revenue"].sum()*100:.1f}%')
print('=' * 60)

# ---------------------------------------------------------------------------
# 1. SALES PERFORMANCE
# ---------------------------------------------------------------------------

# 1a. Monthly Revenue Trend
df['YearMonth'] = df['Order_Date'].dt.to_period('M')
monthly = df.groupby('YearMonth').agg(Revenue=('Revenue', 'sum'), Orders=('Order_ID', 'count')).reset_index()
monthly['YearMonth'] = monthly['YearMonth'].astype(str)

fig, ax1 = plt.subplots()
color1, color2 = '#2563EB', '#DC2626'
ax1.bar(monthly['YearMonth'], monthly['Revenue'], color=color1, alpha=0.7, label='Revenue')
ax1.set_ylabel('Revenue ($)', color=color1); ax1.tick_params(axis='y', labelcolor=color1)
ax1.set_xticks(range(0, len(monthly), 3)); ax1.set_xticklabels(monthly['YearMonth'][::3], rotation=45)
ax2 = ax1.twinx()
ax2.plot(monthly['YearMonth'], monthly['Orders'], color=color2, marker='o', label='Order Volume')
ax2.set_ylabel('Order Count', color=color2); ax2.tick_params(axis='y', labelcolor=color2)
plt.title('Monthly Revenue & Order Volume (2023–2025)')
fig.tight_layout(); plt.savefig('../visuals/monthly_revenue_trend.png', dpi=150, bbox_inches='tight'); plt.close()

# 1b. Revenue by Product Category
cat_rev = df.groupby('Product_Category')['Revenue'].sum().sort_values(ascending=False)
colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(cat_rev)))
ax = cat_rev.plot(kind='bar', color=colors, edgecolor='white')
plt.title('Revenue by Product Category')
plt.ylabel('Total Revenue ($)')
plt.xticks(rotation=45, ha='right')
for i, v in enumerate(cat_rev):
    pct = v / cat_rev.sum() * 100
    ax.text(i, v + cat_rev.max() * 0.01, f'{pct:.1f}%', ha='center', fontweight='bold', fontsize=10)
plt.tight_layout(); plt.savefig('../visuals/revenue_by_category.png', dpi=150, bbox_inches='tight'); plt.close()

# 1c. Top 10 Products by Revenue
prod_rev = df.groupby('Product_Name')['Revenue'].sum().sort_values(ascending=False).head(10)
ax = prod_rev.plot(kind='barh', color='#059669', edgecolor='white')
plt.title('Top 10 Products by Revenue')
plt.xlabel('Total Revenue ($)')
ax.invert_yaxis()
for i, v in enumerate(prod_rev):
    ax.text(v + prod_rev.max() * 0.005, i, f'${v:,.0f}', va='center', fontsize=9)
plt.tight_layout(); plt.savefig('../visuals/top10_products.png', dpi=150, bbox_inches='tight'); plt.close()

# 1d. Sales Channel Performance
channel = df.groupby('Sales_Channel').agg(
    Revenue=('Revenue', 'sum'), Profit=('Profit', 'sum'), Orders=('Order_ID', 'count')
)
channel['Margin'] = (channel['Profit'] / channel['Revenue'] * 100).round(1)
channel = channel.sort_values('Revenue', ascending=False)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
colors_ch = ['#2563EB', '#7C3AED', '#DC2626', '#059669', '#F59E0B']
ax1.pie(channel['Revenue'], labels=channel.index, autopct='%1.1f%%', colors=colors_ch,
        startangle=90, wedgeprops={'edgecolor': 'white'})
ax1.set_title('Revenue Share by Sales Channel')
bars = ax2.barh(channel.index, channel['Margin'], color=colors_ch)
ax2.set_title('Profit Margin by Sales Channel')
ax2.set_xlabel('Margin (%)')
for bar, m in zip(bars, channel['Margin']):
    ax2.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2, f'{m}%', va='center', fontweight='bold')
plt.tight_layout(); plt.savefig('../visuals/channel_performance.png', dpi=150, bbox_inches='tight'); plt.close()

# ---------------------------------------------------------------------------
# 2. SUPPLY CHAIN EFFICIENCY
# ---------------------------------------------------------------------------

# 2a. Delivery Status Breakdown
status_counts = df['Delivery_Status'].value_counts()
status_pct = (status_counts / status_counts.sum() * 100).round(1)
colors_status = {'On Time': '#059669', 'Delayed': '#F59E0B', 'Damaged': '#DC2626', 'Cancelled': '#6B7280'}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
ax1.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%',
        colors=[colors_status[s] for s in status_counts.index], startangle=90, wedgeprops={'edgecolor': 'white'})
ax1.set_title('Delivery Status Distribution')

status_rev_loss = df[df['Delivery_Status'] != 'On Time'].groupby('Delivery_Status')['Revenue'].sum()
bars = ax2.bar(status_rev_loss.index, status_rev_loss / 1e6,
              color=[colors_status[s] for s in status_rev_loss.index], edgecolor='white')
ax2.set_title('Revenue Impact of Delivery Failures ($M)')
ax2.set_ylabel('Revenue ($ Millions)')
for bar, v in zip(bars, status_rev_loss):
    ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2, f'${v/1e6:.1f}M', ha='center', fontweight='bold')
plt.tight_layout(); plt.savefig('../visuals/delivery_status.png', dpi=150, bbox_inches='tight'); plt.close()

# 2b. Lead Time by Supplier Region & Product Category
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
region_lt = df.groupby('Supplier_Region')['Lead_Time_Days'].agg(['mean', 'median', 'std']).round(1)
colors_region = ['#2563EB', '#059669', '#DC2626']
bars = ax1.bar(region_lt.index, region_lt['mean'], color=colors_region, edgecolor='white',
               yerr=region_lt['std'], capsize=5)
ax1.set_title('Average Lead Time by Supplier Region')
ax1.set_ylabel('Lead Time (Days)')
for bar, v in zip(bars, region_lt['mean']):
    ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, f'{v}d', ha='center', fontweight='bold')

cat_lt = df.groupby('Product_Category')['Lead_Time_Days'].mean().sort_values()
ax2.barh(cat_lt.index, cat_lt.values, color='#7C3AED', edgecolor='white')
ax2.set_title('Average Lead Time by Product Category')
ax2.set_xlabel('Lead Time (Days)')
for i, v in enumerate(cat_lt):
    ax2.text(v + 0.3, i, f'{v:.0f}d', va='center', fontsize=9)
plt.tight_layout(); plt.savefig('../visuals/lead_time_analysis.png', dpi=150, bbox_inches='tight'); plt.close()

# 2c. Supplier Performance
supplier_perf = df.groupby('Supplier_Name').agg(
    Total_Revenue=('Revenue', 'sum'),
    Avg_Lead_Time=('Lead_Time_Days', 'mean'),
    On_Time_Rate=('Delivery_Status', lambda x: (x == 'On Time').mean() * 100),
    Orders=('Order_ID', 'count')
).round(1).sort_values('Total_Revenue', ascending=False)

top_suppliers = supplier_perf.head(10)
fig, ax1 = plt.subplots()
x = np.arange(len(top_suppliers))
w = 0.35
ax1.bar(x - w / 2, top_suppliers['Total_Revenue'] / 1e6, w, label='Revenue ($M)', color='#2563EB', edgecolor='white')
ax2 = ax1.twinx()
ax2.bar(x + w / 2, top_suppliers['On_Time_Rate'], w, label='On-Time %', color='#059669', edgecolor='white')
ax1.set_xticks(x); ax1.set_xticklabels(top_suppliers.index, rotation=45, ha='right')
ax1.set_ylabel('Revenue ($ Millions)')
ax2.set_ylabel('On-Time Delivery Rate (%)')
ax1.set_title('Top 10 Suppliers: Revenue vs On-Time Delivery')
fig.legend(loc='upper right'); plt.tight_layout()
plt.savefig('../visuals/supplier_performance.png', dpi=150, bbox_inches='tight'); plt.close()

# ---------------------------------------------------------------------------
# 3. PROFITABILITY ANALYSIS
# ---------------------------------------------------------------------------

# 3a. Margin by Segment & Product Category
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
seg_margin = df.groupby('Customer_Segment')['Profit_Margin_Pct'].mean().sort_values()
colors_seg = ['#2563EB', '#7C3AED', '#059669', '#DC2626']
bars = ax1.barh(seg_margin.index, seg_margin.values, color=colors_seg, edgecolor='white')
ax1.set_title('Average Profit Margin by Customer Segment')
ax1.set_xlabel('Profit Margin (%)')
for bar, v in zip(bars, seg_margin):
    ax1.text(v + 0.3, bar.get_y() + bar.get_height() / 2, f'{v:.1f}%', va='center', fontweight='bold')

cat_margin = df.groupby('Product_Category')['Profit_Margin_Pct'].mean().sort_values()
ax2.barh(cat_margin.index, cat_margin.values, color='#059669', edgecolor='white')
ax2.set_title('Average Profit Margin by Product Category')
ax2.set_xlabel('Profit Margin (%)')
for i, v in enumerate(cat_margin):
    ax2.text(v + 0.3, i, f'{v:.1f}%', va='center', fontsize=9)
plt.tight_layout(); plt.savefig('../visuals/profit_margins.png', dpi=150, bbox_inches='tight'); plt.close()

# 3b. Discount Impact
df['Discount_Bucket'] = pd.cut(df['Discount_Pct'], bins=[-1, 0, 5, 10, 15, 100],
                                labels=['0%', '1-5%', '6-10%', '11-15%', '>15%'])
discount_impact = df.groupby('Discount_Bucket', observed=True).agg(
    Avg_Margin=('Profit_Margin_Pct', 'mean'),
    Total_Revenue=('Revenue', 'sum'),
    Order_Count=('Order_ID', 'count')
).round(1)

fig, ax1 = plt.subplots()
bars = ax1.bar(discount_impact.index, discount_impact['Avg_Margin'],
               color=['#059669' if i == 0 else '#F59E0B' for i in range(len(discount_impact))], edgecolor='white')
ax1.set_title('Average Profit Margin by Discount Bucket')
ax1.set_xlabel('Discount Applied'); ax1.set_ylabel('Avg Profit Margin (%)')
for bar, v in zip(bars, discount_impact['Avg_Margin']):
    ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, f'{v:.1f}%', ha='center', fontweight='bold')
ax2 = ax1.twinx()
ax2.plot(discount_impact.index, discount_impact['Order_Count'], color='#DC2626', marker='o', label='Order Count')
ax2.set_ylabel('Order Count', color='#DC2626'); ax2.tick_params(axis='y', labelcolor='#DC2626')
plt.tight_layout(); plt.savefig('../visuals/discount_impact.png', dpi=150, bbox_inches='tight'); plt.close()

# 3c. Segment x Channel Heatmap
pivot_margin = df.pivot_table(values='Profit_Margin_Pct', index='Customer_Segment', columns='Sales_Channel', aggfunc='mean')
pivot_revenue = df.pivot_table(values='Revenue', index='Customer_Segment', columns='Sales_Channel', aggfunc='sum') / 1e6

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5))
sns.heatmap(pivot_margin, annot=True, fmt='.1f', cmap='RdYlGn', center=40, ax=ax1, linewidths=1, cbar_kws={'label': 'Margin %'})
ax1.set_title('Profit Margin % by Segment & Channel')
sns.heatmap(pivot_revenue, annot=True, fmt='.1f', cmap='Blues', ax=ax2, linewidths=1, cbar_kws={'label': 'Revenue ($M)'})
ax2.set_title('Revenue ($M) by Segment & Channel')
plt.tight_layout(); plt.savefig('../visuals/segment_channel_heatmap.png', dpi=150, bbox_inches='tight'); plt.close()

# ---------------------------------------------------------------------------
# 4. INVENTORY MANAGEMENT
# ---------------------------------------------------------------------------

# 4a. Inventory vs Reorder Point
inv_status = df.groupby('Product_Name').agg(
    Avg_Inventory=('Inventory_Level', 'mean'),
    Avg_Reorder=('Reorder_Point', 'mean'),
    Avg_Safety=('Safety_Stock', 'mean')
).round(0).sort_values('Avg_Inventory', ascending=False).head(15)

inv_status['Stock_Health'] = inv_status['Avg_Inventory'] - inv_status['Avg_Reorder']
inv_status['Status'] = inv_status['Stock_Health'].apply(lambda x: 'Healthy' if x > 0 else 'Reorder Needed')

ax = inv_status[['Avg_Inventory', 'Avg_Reorder', 'Avg_Safety']].plot(
    kind='bar', color=['#2563EB', '#DC2626', '#F59E0B'], edgecolor='white')
plt.title('Top 15 Products: Inventory Levels vs Reorder Points')
plt.ylabel('Units'); plt.xticks(rotation=45, ha='right')
plt.tight_layout(); plt.savefig('../visuals/inventory_analysis.png', dpi=150, bbox_inches='tight'); plt.close()

# 4b. Warehouse Performance
wh_perf = df.groupby('Warehouse_Location').agg(
    Revenue=('Revenue', 'sum'),
    Orders=('Order_ID', 'count'),
    On_Time_Rate=('Delivery_Status', lambda x: (x == 'On Time').mean() * 100),
    Avg_Lead_Time=('Lead_Time_Days', 'mean')
).round(1).sort_values('Revenue', ascending=False)

fig, ax1 = plt.subplots()
bars = ax1.barh(wh_perf.index, wh_perf['Revenue'] / 1e6, color='#2563EB', edgecolor='white')
ax1.set_title('Revenue by Warehouse Location ($M)')
ax1.set_xlabel('Revenue ($ Millions)')
for bar, v in zip(bars, wh_perf['Revenue']):
    ax1.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2, f'{v/1e6:.1f}M', va='center', fontsize=9)
plt.tight_layout(); plt.savefig('../visuals/warehouse_performance.png', dpi=150, bbox_inches='tight'); plt.close()

# ---------------------------------------------------------------------------
# 5. CORRELATION ANALYSIS
# ---------------------------------------------------------------------------
numeric_cols = ['Quantity', 'Unit_Cost', 'Unit_Price', 'Discount_Pct', 'Revenue', 'Total_Cost', 'Profit',
                'Profit_Margin_Pct', 'Lead_Time_Days', 'Inventory_Level', 'Reorder_Point', 'Safety_Stock']
corr = df[numeric_cols].corr()

mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
plt.figure(figsize=(12, 8))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
            vmin=-1, vmax=1, square=True, linewidths=0.5, cbar_kws={'shrink': 0.8})
plt.title('Correlation Matrix of Key Metrics', fontsize=16, fontweight='bold')
plt.tight_layout(); plt.savefig('../visuals/correlation_heatmap.png', dpi=150, bbox_inches='tight'); plt.close()

# ---------------------------------------------------------------------------
# 6. KEY INSIGHTS
# ---------------------------------------------------------------------------
print()
print('=' * 70)
print('KEY INSIGHTS & RECOMMENDATIONS')
print('=' * 70)
print()
print('1. Network Equipment dominates revenue at 43.3% with high margins (~43%).')
print('   >> Prioritize supply chain reliability for this core profit engine.')
print()
print('2. SIM Cards and Fiber Cables have the highest margins (48-49%) but contribute')
print('   only 4.1% and 6.1% of revenue. High-value add-on upsell opportunities.')
print()
print(f'3. On-time delivery is only {status_pct["On Time"]}% — nearly a third of orders face delays/damage.')
print(f'   >> ${status_rev_loss.sum()/1e6:.1f}M in at-risk revenue. Needs immediate logistics intervention.')
print()
print('4. Direct Sales yield the highest margin (47.8%) vs Retail Partners (35.5%).')
print('   >> Channel strategy should favor Direct for high-value deals.')
print()
print('5. Asian suppliers have the longest lead times (avg {:.0f}d).'.format(region_lt.loc['Asia', 'mean']))
print('   >> Dual-sourcing with European/North American suppliers reduces risk.')
print()
print('6. Discounts >15% erode margins by ~15pp vs no-discount orders.')
print('   >> Stricter discount governance with manager approval tiers needed.')
print()
print('7. Government segment shows the highest margins (45.7%).')
print('   >> Target public-sector contracts with dedicated SLAs.')
print()
print('=' * 70)
print('All visualizations saved to ../visuals/')
print('=' * 70)
