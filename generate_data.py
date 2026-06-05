import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# 1. Generate Date Range (approx. 7 months of daily data per region)
start_date = datetime(2025, 11, 1)
end_date = datetime(2026, 5, 31)
delta = end_date - start_date
dates = [start_date + timedelta(days=i) for i in range(delta.days + 1)]

# 2. Define categorical dimensions
regions = ['North America', 'Europe', 'Asia-Pacific', 'Latin America']
lead_sources = ['Organic Search', 'Paid Ads', 'Social Media', 'Referrals']

# 3. Build rows by repeating dates for each region to simulate regional daily tracking
data_rows = []
for date in dates:
    # Memeriksa apakah hari ini weekend (Saturday=5, Sunday=6)
    is_weekend = date.weekday() >= 5
    
    for region in regions:
        # Generate correlated metrics based loosely on the region
        if region == 'North America':
            base_revenue = np.random.normal(25000, 4000)
            base_users = np.random.randint(3000, 5000)
        elif region == 'Europe':
            base_revenue = np.random.normal(18000, 3000)
            base_users = np.random.randint(2000, 3800)
        elif region == 'Asia-Pacific':
            base_revenue = np.random.normal(15000, 2500)
            base_users = np.random.randint(1500, 3500)
        else: # Latin America
            base_revenue = np.random.normal(10000, 1500)
            base_users = np.random.randint(800, 2000)
            
        # -----------------------------------------------------------------
        # KOMBINASI LOGIKA BIKIN BEDA (REAL-WORLD PATTERNS)
        # -----------------------------------------------------------------
        
        # LOGIKA 1: Efek Akhir Pekan (Weekend Drop)
        # Menghadirkan pola naik-turun berkala yang indah pada line-chart
        if is_weekend:
            base_revenue *= 0.70  # Revenue turun 30% saat weekend
            base_users *= 0.75    # Traffic turun 25% saat weekend
            
        # LOGIKA 2: Penyuntikan Anomali Kritis Acak (Bahan Early Warning)
        # Kita sengaja merusak data pada 2% hari acak untuk memicu indikator error/warning
        if np.random.rand() < 0.02:
            base_revenue *= 0.35  # Drop parah hingga 65%
            base_users *= 0.40    # Traffic ikut anjlok
            
        # Ensure values stay strictly positive and realistic
        revenue = round(max(1500, base_revenue), 2)
        active_users = int(max(100, base_users))
        lead_source = np.random.choice(lead_sources, p=[0.35, 0.30, 0.20, 0.15])
        
        # LOGIKA 3: Penambahan Kolom Konversi Berdasarkan Distribusi Channel
        # Paid ads dikondisikan punya tingkat konversi lebih tinggi dibanding media sosial
        if lead_source == 'Paid Ads':
            conv_rate = np.random.uniform(0.04, 0.08) # 4% - 8% konversi
        elif lead_source == 'Organic Search':
            conv_rate = np.random.uniform(0.03, 0.05)
        else:
            conv_rate = np.random.uniform(0.01, 0.03)
            
        conversions = int(active_users * conv_rate)
        
        data_rows.append({
            'Date': date.strftime('%Y-%m-%d'),
            'Region': region,
            'Revenue': revenue,
            'Active_Users': active_users,
            'Conversions': conversions, # Kolom baru untuk metrik efisiensi ekstra
            'Lead_Source': lead_source
        })

# 4. Convert to DataFrame and save to CSV
df = pd.DataFrame(data_rows)
df.to_csv('business_sales_data.csv', index=False)

print("Data generation complete with advanced corporate anomalies!")
print(f"Successfully created 'business_sales_data.csv' with {len(df)} rows.")