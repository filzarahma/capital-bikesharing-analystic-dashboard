import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


#######################
# Page configuration
st.set_page_config(
    page_title="Capital Bikeshare DC Dashboard",
    page_icon="🚴🏻‍♀️",
    layout="wide",
    initial_sidebar_state="expanded")

#######################
# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #F0F2F6; /* Warna latar belakang */
    text-align: center;
    padding: 15px 0;
    border-radius: 5px 5px 5px 5px; /* Mengatur radius pada sudut */
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)

# MENYIAPKAN DATAFRAME
def create_daily_bikesharing(main_df):
    daily_bikesharing_df = main_df.groupby('date').agg({
        'total_count': 'sum',
        'number_of_registered_users': 'sum',
        'number_of_casual_users': 'sum',
    }).reset_index()

    # Tambahkan kolom 'day_of_week'
    daily_bikesharing_df['day_of_week'] = daily_bikesharing_df['date'].dt.day_name()

    return daily_bikesharing_df

# LOAD DATASET
all_df = pd.read_csv('./dashboard/all_data.csv', sep=",")

# menyortir nilai berdasarkan tanggal 
all_df.sort_values(by='date', inplace=True)
all_df.reset_index(inplace=True)

# format data to datetime
all_df['date'] = pd.to_datetime(all_df['date']) 

# MEMBUAT KOMPONEN FILTER -> sidebar
min_date = all_df['date'].min()
max_date = all_df['date'].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image('./image/capital-bikeshare-logo.png', clamp=True)
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Date Range', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    # Menambah filter untuk season
    season_category = st.multiselect(
        label="Season",
        options=all_df['season'].unique()
    )
    # Menambah filter untuk weather
    weather_category = st.multiselect(
        label="Weather",
        options=[
            "1: Clear, Few clouds, Partly cloudy, Partly cloudy",
            "2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist",
            "3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds",
            "4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog"
            ]
    )

    st.caption('Copyright (c) filzarahma')

# KONFIGURASI MAIN DATAFRAME
main_df = all_df[(all_df["date"] >= str(start_date)) & (all_df["date"] <= str(end_date))]
if len(season_category) > 0:
    main_df = main_df[main_df['season'].isin(season_category)]

if len(weather_category) > 0:
    main_df = main_df[main_df['weather_condition'].isin([int(i[0]) for i in weather_category])]

# KONFIGURASI SUB DATAFRAME
daily_bikesharing_df = create_daily_bikesharing(main_df)

# MELENGKAPI DASHBOARD DENGAN VISUALISASI DATA
st.header('Capital Bikesharing Dashboard 🚴🏻‍♀️')

# OVERVIEW
st.subheader('Daily Rides Trend')
col = st.columns(3)
with col[0]:
    total_reg = daily_bikesharing_df.number_of_registered_users.sum()
    st.metric('📝 Registered User    ', value=total_reg)
        
with col[1]:
    total_cnt = daily_bikesharing_df.total_count.sum()
    st.metric('👥 Total User    ', value=total_cnt)

with col[2]:
    total_cas = daily_bikesharing_df.number_of_casual_users.sum()
    st.metric('😎 Casual User    ', value=total_cas)

# Menemukan tanggal dengan jumlah penyewaan total tertinggi
max_total = daily_bikesharing_df['total_count'].max()
max_date = daily_bikesharing_df.loc[daily_bikesharing_df['total_count'] == max_total, 'date'].values[0]

# Membuat figure
fig = go.Figure()

# Menambahkan garis untuk total_count
fig.add_trace(go.Scatter(x=daily_bikesharing_df['date'], y=daily_bikesharing_df['total_count'],
                         mode='lines', name='Total Pengguna',
                         line=dict(color='#003092', width=2)))

# Menambahkan garis untuk pengguna casual
fig.add_trace(go.Scatter(x=daily_bikesharing_df['date'], y=daily_bikesharing_df['number_of_casual_users'],
                         mode='lines', name='Pengguna Kasual',
                         line=dict(color='#00879E', width=2)))

# Menambahkan garis untuk pengguna registered
fig.add_trace(go.Scatter(x=daily_bikesharing_df['date'], y=daily_bikesharing_df['number_of_registered_users'],
                         mode='lines', name='Pengguna Terdaftar',
                         line=dict(color='#FFAB5B', width=2)))

# Menyoroti titik dengan total_count tertinggi
fig.add_trace(go.Scatter(x=[max_date], y=[max_total], mode='markers',
                         marker=dict(color='red', size=10, symbol='star'),
                         name=f'Max: {max_total}'))

# Menyesuaikan tata letak
fig.update_layout(
    title='Tren Peminjaman Sepeda per Hari (2011-2012)',
    xaxis_title='Tanggal',
    yaxis_title='Jumlah Sepeda',
    template='plotly_white',
    xaxis=dict(tickangle=45)
)

# Menampilkan plot
st.plotly_chart(fig)

# MONTHLY COUNT RIDES
# Buat kolom baru dengan format "YYYY-MM" untuk pengelompokan
daily_bikesharing_df['year_month'] = daily_bikesharing_df['date'].dt.to_period('M')

# Grouping berdasarkan year_month untuk registered dan casual users
monthly_trend = daily_bikesharing_df.groupby('year_month', as_index=False)[['number_of_registered_users', 'number_of_casual_users']].sum()

# Konversi year_month ke datetime agar bisa diurutkan
monthly_trend['year_month'] = pd.to_datetime(monthly_trend['year_month'].astype(str))

# Mengubah format data menjadi long format agar bisa divisualisasikan dalam satu plot
monthly_trend_melted = monthly_trend.melt(id_vars=['year_month'],
                                          value_vars=['number_of_registered_users', 'number_of_casual_users'],
                                          var_name='user_type', value_name='total_count')

# Mengganti nama user_type agar lebih mudah dibaca di legenda
user_type_mapping = {
    'number_of_registered_users': 'Registered Users',
    'number_of_casual_users': 'Casual Users'
}
monthly_trend_melted['user_type'] = monthly_trend_melted['user_type'].map(user_type_mapping)

# Membuat line plot dengan Plotly
fig = px.line(monthly_trend_melted, x='year_month', y='total_count', color='user_type',
              title='Tren Peminjaman Sepeda per Bulan (Registered vs Casual)',
              labels={'year_month': 'Bulan', 'total_count': 'Total Peminjaman', 'user_type': 'Tipe Pengguna'},
              markers=True)

# Menyesuaikan tampilan sumbu x agar tidak bertabrakan
fig.update_layout(xaxis=dict(tickangle=-45))

# Menampilkan plot
st.plotly_chart(fig)

# WEEKLY COUNT RIDES
# Urutan hari dalam seminggu
days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Menghitung rata-rata jumlah penyewaan berdasarkan hari dalam seminggu untuk setiap jenis pengguna
daily_avg_registered = daily_bikesharing_df.groupby('day_of_week')['number_of_registered_users'].mean().reindex(days_order)
daily_avg_casual = daily_bikesharing_df.groupby('day_of_week')['number_of_casual_users'].mean().reindex(days_order)

# Menghitung jumlah maksimum penyewaan per hari
daily_max_registered = daily_bikesharing_df.groupby('day_of_week')['number_of_registered_users'].max().reindex(days_order)
daily_max_casual = daily_bikesharing_df.groupby('day_of_week')['number_of_casual_users'].max().reindex(days_order)

# Menentukan hari dengan jumlah maksimal tertinggi
max_day_registered = daily_max_registered.idxmax()
max_value_registered = daily_max_registered.max()

max_day_casual = daily_max_casual.idxmax()
max_value_casual = daily_max_casual.max()

# Membuat figure
fig = go.Figure()

# Menambahkan garis tren untuk registered users
fig.add_trace(go.Scatter(x=daily_avg_registered.index, y=daily_avg_registered.values,
                         mode='lines+markers', name='Rata-rata Registered',
                         line=dict(color='#003f5c', width=2),
                         marker=dict(size=6)))

# Menambahkan garis tren untuk casual users
fig.add_trace(go.Scatter(x=daily_avg_casual.index, y=daily_avg_casual.values,
                         mode='lines+markers', name='Rata-rata Casual',
                         line=dict(color='#ffa600', width=2),
                         marker=dict(size=6)))

# Menambahkan bar plot untuk nilai maksimum registered users
fig.add_trace(go.Bar(x=daily_max_registered.index, y=daily_max_registered.values,
                     name='Maksimum Registered',
                     marker=dict(color='#003f5c', opacity=0.6)))

# Menambahkan bar plot untuk nilai maksimum casual users
fig.add_trace(go.Bar(x=daily_max_casual.index, y=daily_max_casual.values,
                     name='Maksimum Casual',
                     marker=dict(color='#ffa600', opacity=0.6)))

# Menyoroti hari dengan penyewaan tertinggi untuk registered
fig.add_trace(go.Scatter(x=[max_day_registered], y=[max_value_registered], mode='markers',
                         marker=dict(color='#003092', size=10, symbol='star'),
                         name=f'Max Registered ({max_day_registered} - {max_value_registered})'))

# Menyoroti hari dengan penyewaan tertinggi untuk casual
fig.add_trace(go.Scatter(x=[max_day_casual], y=[max_value_casual], mode='markers',
                         marker=dict(color='#ffa600', size=10, symbol='star'),
                         name=f'Max Casual ({max_day_casual} - {max_value_casual})'))

# Menyesuaikan tata letak
fig.update_layout(
    title="Rata-rata dan Maksimum Penyewaan Sepeda per Hari (Registered vs Casual)",
    xaxis_title="Hari",
    yaxis_title="Jumlah Penyewaan",
    xaxis=dict(categoryorder="array", categoryarray=days_order),  # Mengurutkan hari dengan benar
    template='plotly_white',
    barmode='overlay'  # Untuk menumpuk line plot dan bar plot
)

# Menampilkan plot
st.plotly_chart(fig)

# HOURLY COUNT RIDES
# Menghitung rata-rata dan nilai maksimal total_count per jam berdasarkan jenis pengguna
hourly_avg_registered = main_df.groupby('hour')['number_of_registered_users'].mean()
hourly_avg_casual = main_df.groupby('hour')['number_of_casual_users'].mean()

hourly_max_registered = main_df.groupby('hour')['number_of_registered_users'].max()
hourly_max_casual = main_df.groupby('hour')['number_of_casual_users'].max()

# Menentukan jam dengan jumlah maksimal tertinggi
max_hour_registered = hourly_max_registered.idxmax()
max_value_registered = hourly_max_registered.max()

max_hour_casual = hourly_max_casual.idxmax()
max_value_casual = hourly_max_casual.max()

# Membuat figure
fig = go.Figure()

# Menambahkan garis tren untuk registered users
fig.add_trace(go.Scatter(x=hourly_avg_registered.index, y=hourly_avg_registered.values,
                         mode='lines+markers', name='Rata-rata Registered',
                         line=dict(color='#003f5c', width=2),
                         marker=dict(size=6)))

# Menambahkan garis tren untuk casual users
fig.add_trace(go.Scatter(x=hourly_avg_casual.index, y=hourly_avg_casual.values,
                         mode='lines+markers', name='Rata-rata Casual',
                         line=dict(color='#ffa600', width=2),
                         marker=dict(size=6)))

# Menambahkan bar plot untuk nilai maksimum registered users
fig.add_trace(go.Bar(x=hourly_max_registered.index, y=hourly_max_registered.values,
                     name='Maksimum Registered',
                     marker=dict(color='#003f5c', opacity=0.6)))

# Menambahkan bar plot untuk nilai maksimum casual users
fig.add_trace(go.Bar(x=hourly_max_casual.index, y=hourly_max_casual.values,
                     name='Maksimum Casual',
                     marker=dict(color='#ffa600', opacity=0.6)))

# Menyoroti jam dengan penyewaan tertinggi untuk registered
fig.add_trace(go.Scatter(x=[max_hour_registered], y=[max_value_registered], mode='markers',
                         marker=dict(color='#003092', size=10, symbol='star'),
                         name=f'Max Registered ({max_hour_registered}:00 - {max_value_registered})'))

# Menyoroti jam dengan penyewaan tertinggi untuk casual
fig.add_trace(go.Scatter(x=[max_hour_casual], y=[max_value_casual], mode='markers',
                         marker=dict(color='#ffa600', size=10, symbol='star'),
                         name=f'Max Casual ({max_hour_casual}:00 - {max_value_casual})'))

# Menyesuaikan tata letak
fig.update_layout(
    title="Rata-rata dan Maksimum Penyewaan Sepeda per Jam (Registered vs Casual)",
    xaxis_title="Jam",
    yaxis_title="Jumlah Penyewaan",
    xaxis=dict(tickmode='array', tickvals=list(range(24))),
    template='plotly_white',
    barmode='overlay'  # Untuk menumpuk line plot dan bar plot
)

# Menampilkan plot
st.plotly_chart(fig)

# SEASON COUNT RIDES
import plotly.graph_objects as go
import pandas as pd

# Menghitung total penyewaan berdasarkan musim untuk registered & casual users
season_total = main_df.groupby('season', as_index=False)[['number_of_registered_users', 'number_of_casual_users']].sum()

# Warna untuk masing-masing kategori
color_registered = '#FFAB5B'
color_casual = '#FFC300'

# Membuat figure
fig = go.Figure()

# Bar plot untuk registered users
fig.add_trace(go.Bar(
    x=season_total['season'],
    y=season_total['number_of_registered_users'],
    name="Registered Users",
    marker=dict(color=color_registered),
    text=season_total['number_of_registered_users'].round(2),
    textposition='auto'
))

# Bar plot untuk casual users
fig.add_trace(go.Bar(
    x=season_total['season'],
    y=season_total['number_of_casual_users'],
    name="Casual Users",
    marker=dict(color=color_casual),
    text=season_total['number_of_casual_users'].round(2),
    textposition='auto'
))

# Menyesuaikan tata letak menjadi stacked bar
fig.update_layout(
    title="Total Penyewaan Sepeda Berdasarkan Musim (Registered vs Casual)",
    xaxis_title="Musim",
    yaxis_title="Total Peminjaman",
    barmode='stack',  # Mengubah mode menjadi 'stack'
    template='plotly_white'
)

# Menampilkan plot
st.plotly_chart(fig)


# WEATHER COUNT RIDES

# Menghitung jumlah penyewaan per musim
weather_sum = main_df.groupby('weather_condition', as_index=False)['total_count'].sum()

# Menentukan musim dengan nilai tertinggi
max_weather = weather_sum.loc[weather_sum['total_count'].idxmax(), 'weather_condition']  # Musim dengan rata-rata penyewaan tertinggi
max_value = weather_sum['total_count'].max()  # Nilai rata-rata tertinggi

# Warna untuk setiap musim (standar: orange, tertinggi: biru)
colors = ['#FFAB5B' if weather != max_weather else '#00879E' for weather in weather_sum['weather_condition']]

# Membuat bar plot
fig = go.Figure()

fig.add_trace(go.Bar(
    x=weather_sum['weather_condition'],  # Gunakan nama musim langsung
    y=weather_sum['total_count'],
    marker=dict(color=colors),  # Gunakan warna berbeda untuk musim dengan penyewaan tertinggi
    text=weather_sum['total_count'].round(2),  # Menampilkan nilai pada bar
    textposition='auto',
    name='Total Penyewaan'
))

# Menyesuaikan tata letak
fig.update_layout(
    title="Total Penyewaan Sepeda Berdasarkan Cuaca",
    xaxis_title="Cuaca",
    yaxis_title="Tota Jumlah Penyewaan",
    template='plotly_white'
)

# Menampilkan plot
st.plotly_chart(fig)

# FACETGRID SEASON VS WEATHER
# Membuat histogram menggunakan Plotly Express
fig = px.histogram(main_df, x="total_count", 
                   facet_col="season", facet_row="weather_condition",
                   color="season", 
                   title="Total Peminjaman Sepeda Berdasrkan situasi cuaca dan musim",
                   labels={"total_count": "Count", "weather_condition": "Weather Condition", "season": "Season"},
                   opacity=0.7,
                   nbins=30)  # Menentukan jumlah bin dalam histogram

# Menyesuaikan tata letak agar lebih rapi
fig.update_layout(
    height=1600,  # Menyesuaikan tinggi gambar
    width=2000,  # Menyesuaikan lebar gambar
    showlegend=False,  # Menyembunyikan legenda karena sudah terlihat dalam judul facet
    title_x=0.5  # Pusatkan judul
)

# Menampilkan plot
st.plotly_chart(fig)