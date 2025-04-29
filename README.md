# Capital Bikeshare Dashboard 🚴🏻‍♀️

![Capital Bikeshare Logo](./image/capital-bikeshare-logo.png)

## Project Overview
This project analyzes bike sharing data from the Capital Bikeshare system in Washington DC for the years 2011-2012. Through comprehensive data analysis and interactive visualization, the dashboard provides insights into bike rental patterns based on time, weather conditions, seasons, and user types.

## Dataset
The dataset contains hourly and daily bike rental counts between 2011 and 2012, with information including:
- Date and time information
- Weather conditions (temperature, humidity, windspeed)
- Season information
- Holiday/weekend flags
- Casual and registered user counts

## Key Findings
- **Yearly Trends**: Bike rentals increased from 2011 to 2012, with seasonal patterns showing higher usage in summer and fall.
- **Daily Patterns**: Peak usage occurs during commuting hours (7-9 AM and 5-7 PM), particularly on weekdays.
- **Seasonal Impact**: Fall has the highest rental rates, followed by summer, winter, and spring with the lowest.
- **Weather Influence**: Clear weather significantly increases rentals, while poor weather conditions drastically reduce usage.
- **User Type Differences**: Registered users mainly ride during weekdays for commuting, while casual users prefer weekends for recreational purposes.

## Dashboard Features
The interactive Streamlit dashboard includes:
- **Time filters**: Select specific date ranges for analysis
- **Condition filters**: Filter by season and weather conditions
- **Visualizations**:
  - Daily and monthly rental trends
  - Hourly usage patterns
  - Day of week comparisons
  - Seasonal and weather impact analysis
  - User type distribution (casual vs. registered)

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run Streamlit Dashboard
```
streamlit run dashboard/dashboard.py
```

## Project Structure
```
bike-sharing-dashboard/
├── dashboard/
│   ├── dashboard.py      # Streamlit dashboard code
│   └── all_data.csv      # Processed dataset for the dashboard
├── image/
│   └── capital-bikeshare-logo.png  # Logo for the dashboard
├── Proyek_Analisis_Data_bike_sharing.ipynb  # Data analysis notebook
├── README.md             # Project documentation
└── requirements.txt      # Required packages
```

## Author
- **Name:** Filza Rahma Muflihah
- **Email:** filzarahmamuflihah@gmail.com
- **ID Dicoding:** filza_rahma_muflihah

## Screenshots
(Dashboard screenshots would be displayed here)
