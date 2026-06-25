# ==========================================
# DASHBOARD OPERATION EXCELLENCE 2026
# Menggunakan Streamlit
# ==========================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")

# Judul Dashboard
st.set_page_config(page_title="Operation Excellence 2026", layout="wide")
st.title("📊 Dashboard Operation Excellence 2026")
st.markdown("---")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('data_bersih_operation_excellence.csv')
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    return df

df = load_data()

# ==========================================
# SIDEBAR FILTER
# ==========================================
st.sidebar.header("🎯 Filter")

# Filter Tanggal
min_date = df['Tanggal'].min()
max_date = df['Tanggal'].max()
date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range
    df_filtered = df[(df['Tanggal'] >= pd.to_datetime(start_date)) & 
                     (df['Tanggal'] <= pd.to_datetime(end_date))]
else:
    df_filtered = df

# Filter Mesin
mesin_list = ['Semua'] + df['Nama_Mesin'].unique().tolist()
selected_mesin = st.sidebar.selectbox("Pilih Mesin", mesin_list)

if selected_mesin != 'Semua':
    df_filtered = df_filtered[df_filtered['Nama_Mesin'] == selected_mesin]

# Filter Shift
shift_list = ['Semua'] + df['Grup_Shift'].unique().tolist()
selected_shift = st.sidebar.selectbox("Pilih Shift", shift_list)

if selected_shift != 'Semua':
    df_filtered = df_filtered[df_filtered['Grup_Shift'] == selected_shift]

# ==========================================
# METRIK / SCORECARD
# ==========================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📦 Total Output", f"{df_filtered['Output_Qty_OK'].sum():,}")

with col2:
    st.metric("❌ Total Reject", f"{df_filtered['Reject_Qty_NG'].sum():,}")

with col3:
    reject_ratio = (df_filtered['Reject_Qty_NG'].sum() / df_filtered['Output_Qty_OK'].sum()) * 100
    st.metric("📊 Reject Ratio", f"{reject_ratio:.2f}%")

with col4:
    st.metric("📋 Total Data", f"{len(df_filtered):,}")

st.markdown("---")

# ==========================================
# GRAFIK 1: BOTTLENECK (Reject per Mesin)
# ==========================================
st.subheader("🔴 1. Bottleneck Stamping (Reject per Mesin)")

bottleneck = df_filtered.groupby('Nama_Mesin')['Reject_Qty_NG'].sum().sort_values(ascending=False)
fig1, ax1 = plt.subplots(figsize=(10, 5))
bottleneck.plot(kind='bar', color='coral', ax=ax1)
ax1.set_title('Total Reject per Mesin')
ax1.set_xlabel('Nama Mesin')
ax1.set_ylabel('Total Reject')
ax1.tick_params(axis='x', rotation=45)
st.pyplot(fig1)

# ==========================================
# GRAFIK 2: ANOMALI SHIFT B
# ==========================================
st.subheader("📊 2. Anomali Shift B (Reject per Shift)")

shift_reject = df_filtered.groupby('Grup_Shift')['Reject_Qty_NG'].sum()
fig2, ax2 = plt.subplots(figsize=(8, 5))
shift_reject.plot(kind='bar', color=['blue', 'red', 'green'], ax=ax2)
ax2.set_title('Total Reject per Shift')
ax2.set_xlabel('Grup Shift')
ax2.set_ylabel('Total Reject')
st.pyplot(fig2)

# ==========================================
# GRAFIK 3: TREN OUTPUT HARIAN
# ==========================================
st.subheader("📈 3. Tren Output Harian")

daily_output = df_filtered.groupby('Tanggal')['Output_Qty_OK'].sum()
fig3, ax3 = plt.subplots(figsize=(12, 5))
daily_output.plot(color='blue', linewidth=2, ax=ax3)
ax3.set_title('Tren Output Harian')
ax3.set_xlabel('Tanggal')
ax3.set_ylabel('Total Output')
ax3.tick_params(axis='x', rotation=45)
st.pyplot(fig3)

# ==========================================
# GRAFIK 4: KORELASI RPM vs REJECT
# ==========================================
st.subheader("🔍 4. Korelasi RPM vs Reject")

fig4, ax4 = plt.subplots(figsize=(10, 6))
scatter = ax4.scatter(
    df_filtered['Setting_Speed_RPM'],
    df_filtered['Reject_Qty_NG'],
    c=df_filtered['Skill_Level'],
    cmap='viridis',
    alpha=0.6
)
ax4.set_title('RPM vs Reject (warna = Skill Level)')
ax4.set_xlabel('Setting Speed (RPM)')
ax4.set_ylabel('Reject (Qty NG)')
plt.colorbar(scatter, label='Skill Level')
st.pyplot(fig4)

# ==========================================
# GRAFIK 5: TOP 5 OPERATOR
# ==========================================
st.subheader("👷 5. Top 5 Operator dengan Reject Tertinggi")

top_operators = df_filtered.groupby('Nama_Lengkap')['Reject_Qty_NG'].sum().sort_values(ascending=False).head(5)
fig5, ax5 = plt.subplots(figsize=(10, 5))
top_operators.plot(kind='bar', color='purple', ax=ax5)
ax5.set_title('Top 5 Operator dengan Reject Tertinggi')
ax5.set_xlabel('Nama Operator')
ax5.set_ylabel('Total Reject')
ax5.tick_params(axis='x', rotation=45)
st.pyplot(fig5)

st.markdown("---")
st.caption("Dashboard Operation Excellence 2026 - PT Andalas Manufaktur")